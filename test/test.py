
def zsq(func):
    print "before"
    func()
    print "after"
    return func
@zsq
def test1():
    print "hehe"

test1()