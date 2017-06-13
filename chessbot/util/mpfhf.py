def mpfhf(text, control_pattern):
    mpfhfcall = text.split(' ', 2)
    if len(mpfhfcall) > 2:
        bits = int(mpfhfcall[1])
        message = mpfhfcall[2]
        if bits > 0 and bits <= 128:
            return "Proceeding with %d-bit hash of: %s" % (bits, message)
        else:
            return "I only hash up to 128-bits."
    else:
        return "Please call me in the format: %smpfhf <bits> <message>" % control_pattern
