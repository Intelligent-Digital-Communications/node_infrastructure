for i in {1..24}
do
	at -f python3 manage.py test myapp.tests.GetATQTestCase now + $i hour >> atqdata.txt
done