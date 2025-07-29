from topoly import draw_tangle
import logging #not using currently, also there is no boolean "debug" argument right now
import os

log = logging.getLogger()

def run_test(tangle_str, expected, name = ""):
    error_codes = ["No error", "Invalid tangle_str", "Invalid file name"]

    if len(error_codes) <= expected or expected < 0:
        log.info("Invalid test, expected =", expected, "is an incorrect value.")

    log.info("tangle_str=" + tangle_str + '; ' + "name=" + name + '; ' + "expected outcome:" + error_codes[expected])
    return_value = draw_tangle(tangle_str, name)
    assert (return_value < len(error_codes) or return_value < 0), "Invalid return code"
    log.info(" outcome: " + error_codes[return_value])
    assert return_value == expected, "Incorrect return code"


def test_drawing():
    log.info("Testing tangle drawing")
    logging.getLogger('matplotlib.font_manager').disabled = True
    tangle_str = "(1,3,(2,3))" #input from original Bostjan's code
    names = ["nice_name", "__00--00__", "_,_"]
    result = draw_tangle(tangle_str)
    assert result == 0 #checks for error codes
    run_test(tangle_str, 0, names[0]) #ADD checking if files exist/aren't empty
    run_test(tangle_str, 0, names[1])
    run_test(tangle_str, 2, names[2]) #forbidden character (comma)
    run_test("(definitely, not, a, valid, tangle_str)", 1)
    run_test("1", 0) # seems to be a valid tangle tuple?

    filenames = ["1323.svg", "nice_name.svg", "__00--00__.svg", "1.svg"]
    for name in filenames:
        log.info("Check if file " + name + " exists and is not empty.")
        assert os.path.isfile("api/download/SVGs/" + name), "File not found."
        assert os.path.getsize("api/download/SVGs/" + name), "File is empty."

if __name__ == "__main__":
    test_drawing()
