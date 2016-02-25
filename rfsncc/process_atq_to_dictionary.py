import subprocess
def process_atq_to_dict():
    id_timedate_dict = {}
    p = subprocess.Popen(
            'atq',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
            )
    output, err = p.communicate() # Catch output in these vars
    for line in output.split('\n'):
        if line == '':
            return id_timedate_dict

        # could split on 'a' queue, but might not always be in 'a' queue.
        # So we have to do it the hard way.
        misc = line.split('\t')
        jobid = misc[0]
        timedate_list = misc[1].split(' ')[0:5]
        timedate_string = ' '.join(timedate_list)
        # to parse this string into a datetime object,
        # import datetime from datetime
        # datetime.strptime(job_misc[1], "%c")
        id_timedate_dict[jobid] = timedate_string


for jobid, datetime in process_atq_to_dict().iteritems():
    print('jobid ' + jobid + ' scheduled to run at ' + datetime)
