# lame.pxd

# Declare external C definitions from lame/lame.h
cdef extern from "<lame/lame.h>":

    # Declare the forward-declared struct hip_global_struct.
    # We use 'pass' because we don't need to access its internal members in Cython.
    # This matches the 'struct hip_global_struct;' line in lame.h
    cdef struct hip_global_struct:
        pass

    # Declare the typedef for struct hip_global_struct as hip_global_flags.
    # This matches the 'typedef struct hip_global_struct hip_global_flags;' line in lame.h
    ctypedef hip_global_struct hip_global_flags

    # Declare the typedef for the pointer to hip_global_flags as hip_t.
    # This correctly defines hip_t as a pointer type in Cython,
    # matching the 'typedef hip_global_flags *hip_t;' line in lame.h
    ctypedef hip_global_flags* hip_t

    # Declare other LAME API functions you use from lame.h.
    # Ensure the function signatures match the C header, using hip_t (the pointer type)
    # where appropriate for handles.

    # Example function declarations (adjust based on actual lame.h signatures):
    hip_t hip_decode_init() nogil
    int hip_decode_exit(hip_t hip_handle) nogil
    int hip_decode1(
        hip_t hip_handle,
        unsigned char* mp3_buffer,
        size_t len,
        short* pcm_l,
        short* pcm_r) nogil

    # Other lame api functions (from your original pxd)
    int lame_get_bitrate(int mpeg_version, int table_index) nogil
    int lame_get_samplerate(int mpeg_version, int table_index) nogil

    # Add any other declarations from lame.h that your wrapper uses.
