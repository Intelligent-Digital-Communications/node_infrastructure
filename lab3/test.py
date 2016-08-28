import hug

@hug.post('/this/is/a/really/bad/request/mapping/test')
def testpost(name, number):
    labname = 'Hayden'
    return "Hi {}, your number was {}, and I'm {}".format(name, number, labname)
