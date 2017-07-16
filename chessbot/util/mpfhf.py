def mpfhf(text, control_pattern):
    mpfhfcall = text.split(' ', 2)
    if len(mpfhfcall) != 3:
        return "Please call me in the format: %smpfhf <bits> <message>" % control_pattern

    bits = int(mpfhfcall[1])
    message = mpfhfcall[2]
    if not (bits > 0 and bits <= 128):
        return "I only hash up to 128-bits."

    return "Proceeding with %d-bit hash of: %s" % (bits, message)
