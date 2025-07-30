""" lame hip decoding wrapper for python """

cimport lame

cdef class Hip:
    """ hip decoder class

    This class maintains the data structures needed for decoding MP3
    frames and encapsulates the hip encoder api.

    """

    cdef lame.hip_t hip_handle # Renamed for clarity

    def __cinit__(self):
        # hip_decode_init returns a hip_t (a pointer), assign it to the pointer variable
        self.hip_handle = lame.hip_decode_init()
        # In C, a NULL pointer indicates failure, which translates to Python's None
        if not self.hip_handle:
            raise MemoryError("Failed to initialize LAME HIP decoder")

    def __dealloc__(self):
        # Pass the hip_t pointer to the exit function
        if self.hip_handle: # Check if the pointer is not NULL
            lame.hip_decode_exit(self.hip_handle)
            # Set the pointer to NULL after freeing to avoid double freeing
            self.hip_handle = NULL # You might need to cimport NULL from libc.stdlib or similar

    def decode(self,
               mp3_buffer,
               mp3_length,
               pcm_lbuffer,
               pcm_rbuffer):
        """ decode an mp3 frame into left/right 16-bit pcm buffers

        Args:
            mp3_buffer (bytes): buffer containing a whole mp3 frame
            mp3_length (int): the number of bytes in the frame
            pcm_lbuffer (bytearray): return left channel pcm samples via here
            pcm_rbuffer (bytearray): return right channel pcm samples via here

        Returns:
            decoded (int): the number of pcm bytes decoded into each channel
                buffer

        """
        return self.do_decode(mp3_buffer,
                              mp3_length,
                              pcm_lbuffer,
                              pcm_rbuffer) * 2

    cdef int do_decode(self,
                       unsigned char* mp3_buffer,
                       size_t mp3_length,
                       unsigned char* pcm_lbuffer,
                       unsigned char* pcm_rbuffer):
        # Pass the hip_t pointer to the decode function
        # Cast pcm_lbuffer and pcm_rbuffer to short* is correct as per the pxd declaration
        return lame.hip_decode1(self.hip_handle,
                                mp3_buffer,
                                mp3_length,
                                <short*>pcm_lbuffer,
                                <short*>pcm_rbuffer)


def get_bit_rate(version, index):
    """ map an mp3 version/bitrate code to a kbps value

    Args:
        version (int): mp3g version (0=mpeg-2, 1=mpeg-1, 2=mpeg-2.5)
        index (int): bitrate code (0-15)

    Returns:
        bitrate (int): the kbps rate of the mp3 frame

    """
    return lame.lame_get_bitrate(version, index)


def get_sample_rate(version, index):
    """ map an mp3 version/bitrate code to a sample rate value

    Args:
        version (int): mp3g version (0=mpeg-2, 1=mpeg-1, 2=mpeg-2.5)
        index (int): bitrate code (0-15)

    Returns:
        sample_rate (int): audio sample rate (Hz)

    """
    return lame.lame_get_samplerate(version, index)
