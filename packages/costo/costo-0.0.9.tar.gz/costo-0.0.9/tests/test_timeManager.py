import costo.timeManager as COT
import traceback

def sould_not_be_called():
    raise RuntimeError

def test_clock():
    clock = COT.clock(t0=0)
    clock.increment(2.)
    assert clock.time == 2.
    clock.increment(2.)
    assert clock.time == 4.
    clock.reset(1.)
    assert clock.time == 1.
    clock.increment(2.)
    assert clock.time == 3.

    # try to set protected atribut time
    try:
        clock.time = 2
        sould_not_be_called()
    except:
        print()
        print("-"*50)
        print('Dont worry, the following exception is a normal behavior')
        print("-"*50)
        ret = traceback.format_exc()
        assert "RuntimeError: Time can't be set, use reset or increment" in ret
        print(ret)
        print("-"*50)
        pass

    # try to acces to an non existing attribut (times)
    try:
        clock.times = 2
        sould_not_be_called()
    except:
        print()
        print("-"*50)
        print('Dont worry, the following exception is a normal behavior')
        print("-"*50)
        ret = traceback.format_exc()
        assert "AttributeError: 'clock' object has no attribute 'times'" in ret
        print(ret)
        print("-"*50)
        pass
