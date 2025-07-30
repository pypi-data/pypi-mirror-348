import ctypes
from ctypes import wintypes
kernel32 = ctypes.windll.kernel32
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010
MEM_COMMIT = 0x1000
PAGE_READWRITE = 0x04
P_A_A=0x1F0FFF
TH32CS_SNAPPROCESS = 0x2
TH32CS_SNAPMODULE=0x00000008
TH32CS_SNAPMODULE32=0x00000010
INVALID_HANDLE_VALUE = -1

class MEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ('BaseAddress',       ctypes.c_void_p),
        ('AllocationBase',    ctypes.c_void_p),
        ('AllocationProtect', wintypes.DWORD),
        ('RegionSize',        ctypes.c_size_t),
        ('State',             wintypes.DWORD),
        ('Protect',           wintypes.DWORD),
        ('Type',              wintypes.DWORD),
    ]

class SYSTEM_INFO(ctypes.Structure):
    _fields_ = [
        ("wProcessorArchitecture", wintypes.WORD),
        ("wReserved", wintypes.WORD),
        ("dwPageSize", wintypes.DWORD),
        ("lpMinimumApplicationAddress", ctypes.c_void_p),
        ("lpMaximumApplicationAddress", ctypes.c_void_p),
        ("dwActiveProcessorMask", ctypes.c_void_p),
        ("dwNumberOfProcessors", wintypes.DWORD),
        ("dwProcessorType", wintypes.DWORD),
        ("dwAllocationGranularity", wintypes.DWORD),
        ("wProcessorLevel", wintypes.WORD),
        ("wProcessorRevision", wintypes.WORD),
    ]
def scan_all_addresses_with_value(pid,value,type='int'):
    all_address=[]
    process_handle = kernel32.OpenProcess(P_A_A, False, pid)
    sys_info = SYSTEM_INFO()
    kernel32.GetSystemInfo(ctypes.byref(sys_info))
    address = sys_info.lpMinimumApplicationAddress
    max_address = sys_info.lpMaximumApplicationAddress
    mbi = MEMORY_BASIC_INFORMATION()
    if type == 'int':
        buffer = ctypes.c_int()
    elif type=='float':
        buffer=ctypes.c_float()
    elif type=='double':
        buffer = ctypes.c_double()
    elif type=='long':
        buffer = ctypes.c_long()
    elif type == 'longlong':
        buffer = ctypes.c_longlong()
    elif type=='string':
        buffer = ctypes.create_string_buffer(4096)
    else:
        return None
    bytes_read = ctypes.c_size_t()
    while address < max_address:
        if kernel32.VirtualQueryEx(process_handle, ctypes.c_void_p(address), ctypes.byref(mbi), ctypes.sizeof(mbi)):
            if mbi.State == MEM_COMMIT and mbi.Protect == PAGE_READWRITE:
                region_start = address
                region_end = address + mbi.RegionSize
                current_address = region_start
                while current_address < region_end:
                    if kernel32.ReadProcessMemory(process_handle, ctypes.c_void_p(current_address), ctypes.byref(buffer), ctypes.sizeof(buffer), ctypes.byref(bytes_read)):
                        if buffer.value == value:
                            all_address.append(current_address)
                    current_address += ctypes.sizeof(buffer)
            address += mbi.RegionSize
        else:
            break
    kernel32.CloseHandle(process_handle)
    return all_address


class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [('dwSize', ctypes.wintypes.DWORD),
                ('cntUsage', ctypes.wintypes.DWORD),
                ('th32ProcessID', ctypes.wintypes.DWORD),
                ('th32DefaultHeapID', ctypes.POINTER(ctypes.wintypes.ULONG)),
                ('th32ModuleID', ctypes.wintypes.DWORD),
                ('cntThreads', ctypes.wintypes.DWORD),
                ('th32ParentProcessID', ctypes.wintypes.DWORD),
                ('pcPriClassBase', ctypes.wintypes.LONG),
                ('dwFlags', ctypes.wintypes.DWORD),
                ('szExeFile', ctypes.c_char * wintypes.MAX_PATH)]


class MODULEENTRY32(ctypes.Structure):
    _fields_ = [
        ('dwSize', wintypes.DWORD),
        ('th32ModuleID', wintypes.DWORD),
        ('th32ProcessID', wintypes.DWORD),
        ('GlblcntUsage', wintypes.DWORD),
        ('ProccntUsage', wintypes.DWORD),
        ('modBaseAddr', ctypes.POINTER(ctypes.c_byte)),
        ('modBaseSize', wintypes.DWORD),
        ('hModule', wintypes.HMODULE),
        ('szModule', ctypes.c_char * (255+ 1)),
        ('szExePath', ctypes.c_char * wintypes.MAX_PATH)
    ]
def getpid(name):
    hSnap = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    procEntry = PROCESSENTRY32()
    procEntry.dwSize = ctypes.sizeof(PROCESSENTRY32)
    while kernel32.Process32Next(hSnap, ctypes.byref(procEntry)):
        if procEntry.szExeFile.decode("utf-8") == name:
            pid = int(procEntry.th32ProcessID)
            return pid
    kernel32.CloseHandle(hSnap)

def is_process_64bit(process_handle):
    is_wow64 = wintypes.BOOL()
    if not kernel32.IsWow64Process(process_handle, ctypes.byref(is_wow64)):
        raise ctypes.WinError()
    return not is_wow64.value
class winmemory():
    def __init__(self,name):
        self.name=name
        self.pid=getpid(self.name)
        self.handle=kernel32.OpenProcess(P_A_A,0,ctypes.wintypes.DWORD(self.pid))
        self.arch=is_process_64bit(self.handle)
        if self.arch:
            self.arch=64
        else:
            self.arch=32

    def get_module_base_address(self,moduleName):
        hSnap = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, self.pid)
        modEntry = MODULEENTRY32()
        modEntry.dwSize = ctypes.sizeof(MODULEENTRY32)
        while (kernel32.Module32Next(hSnap, ctypes.byref(modEntry))):
            if (modEntry.szModule.decode("utf-8") == moduleName):
                baseAddress = int(hex(ctypes.addressof(modEntry.modBaseAddr.contents)), 16)
                return baseAddress
        kernel32.CloseHandle(hSnap)

    def write_int(self,address,value):
        kernel32.WriteProcessMemory(self.handle, ctypes.c_void_p(address),ctypes.byref(ctypes.c_int(value)),ctypes.sizeof(ctypes.c_int),None)

    def read_int(self,address):
        value = ctypes.c_int()
        kernel32.ReadProcessMemory(self.handle, ctypes.c_void_p(address),ctypes.byref(value),ctypes.sizeof(value))
        return value.value

    def write_float(self,address,value):
        kernel32.WriteProcessMemory(self.handle, ctypes.c_void_p(address),ctypes.byref(ctypes.c_float(value)),ctypes.sizeof(ctypes.c_float),None)

    def read_float(self,address):
        value = ctypes.c_float()
        kernel32.ReadProcessMemory(self.handle, ctypes.c_void_p(address),ctypes.byref(value),ctypes.sizeof(value))
        return value.value

    def write_double(self,address,value):
        kernel32.WriteProcessMemory(self.handle, ctypes.c_void_p(address),ctypes.byref(ctypes.c_double(value)),ctypes.sizeof(ctypes.c_double),None)

    def read_double(self, address):
        value = ctypes.c_double()
        kernel32.ReadProcessMemory(self.handle,  ctypes.c_void_p(address), ctypes.byref(value), ctypes.sizeof(value))
        return value.value

    def write_bytes(self, address, data_bytes):
        size = len(data_bytes)
        kernel32.WriteProcessMemory(self.handle, ctypes.c_void_p(address),data_bytes,size)

    def read_bytes(self, address, size):
        read_buffer=ctypes.c_ubyte()
        lp_buffer=ctypes.byref(read_buffer)
        nsize=ctypes.sizeof(read_buffer)
        lp_num=ctypes.c_ulong(0)
        return [hex(read_buffer.value) for x in range(size) if kernel32.ReadProcessMemory(self.handle, ctypes.c_void_p(address + x), lp_buffer,nsize, lp_num)]

    def write_string(self,address,string):
        kernel32.WriteProcessMemory(self.handle, ctypes.c_void_p(address),string.encode()+b'\x00',len(string))

    def read_string(self,address,length=64):
        read_buffer = ctypes.create_string_buffer(length)
        lp_number_of_bytes_read = ctypes.c_ulong(0)
        kernel32.ReadProcessMemory(self.handle, ctypes.c_void_p(address), read_buffer, length,lp_number_of_bytes_read)
        return read_buffer.value.decode('utf-8')

    def write_long(self,address,value):
        kernel32.WriteProcessMemory(self.handle, ctypes.c_void_p(address),ctypes.byref(ctypes.c_long(value)),ctypes.sizeof(ctypes.c_long),None)

    def read_long(self,address):
        value = ctypes.c_long
        kernel32.ReadProcessMemory(self.handle, ctypes.c_void_p(address), ctypes.byref(value), ctypes.sizeof(value))
        return value.value

    def write_longlong(self,address,value):
        kernel32.WriteProcessMemory(self.handle, ctypes.c_void_p(address),ctypes.byref(ctypes.c_longlong(value)),ctypes.sizeof(ctypes.c_longlong),None)

    def read_longlong(self,address):
        value = ctypes.c_longlong
        kernel32.ReadProcessMemory(self.handle, ctypes.c_void_p(address), ctypes.byref(value), ctypes.sizeof(value))
        return value.value

    def write_longdouble(self,address,value):
        kernel32.WriteProcessMemory(self.handle, ctypes.c_void_p(address),ctypes.byref(ctypes.c_longdouble(value)),ctypes.sizeof(ctypes.c_longdouble),None)

    def read_longdouble(self,address):
        value = ctypes.c_longdouble
        kernel32.ReadProcessMemory(self.handle, ctypes.c_void_p(address), ctypes.byref(value), ctypes.sizeof(value))
        return value.value

    def find_pointer_address(self,base,offsets):
        if self.arch==64:
            size=8
        else:
            size=4
        address=ctypes.c_uint64(base)
        for offset in offsets:
            kernel32.ReadProcessMemory(self.handle,address,ctypes.byref(address),size,0)
            address=ctypes.c_uint64(address.value+offset)
        return address.value

