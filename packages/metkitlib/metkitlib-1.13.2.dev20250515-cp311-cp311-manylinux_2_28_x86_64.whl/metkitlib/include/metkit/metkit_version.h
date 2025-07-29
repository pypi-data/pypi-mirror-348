#ifndef metkit_version_h
#define metkit_version_h

#define metkit_VERSION_STR "1.13.2.dev20250515"
#define metkit_VERSION     "1.13.2"

#define metkit_VERSION_MAJOR 1
#define metkit_VERSION_MINOR 13
#define metkit_VERSION_PATCH 2

#define metkit_GIT_SHA1 "8b0cdef44bbdb00a642d75eb75db4bdb16b088e4"

#ifdef __cplusplus
extern "C" {
#endif

const char * metkit_version();

unsigned int metkit_version_int();

const char * metkit_version_str();

const char * metkit_git_sha1();

#ifdef __cplusplus
}
#endif


#endif // metkit_version_h
