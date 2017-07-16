#include <stdio.h>
#include <windows.h>

int main(void) {
	SYSTEM_INFO si;
	GetSystemInfo(&si);
    printf("The minimum address for this system is 0x%p\n", si.lpMinimumApplicationAddress);
    printf("The maximum address for this system is 0x%p\n", si.lpMaximumApplicationAddress);
	printf("The page size for this system is %u bytes.\n", si.dwPageSize);
	return 0;
}