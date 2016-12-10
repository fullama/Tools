def sliding_window(input_list, window_size):
    # Creates tuples of a defined window size from a list
    try:
        for i, element in enumerate(input_list):
                window = input_list[i:i + window_size]
                if len(window) == window_size:
                    yield(window)
                else:
                    return
    except StopIteration:
        return
