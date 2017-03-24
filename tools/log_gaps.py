import simplejson as json
import pandas as pd
import csv

# author Leila
# March 23, 2017

# script to read json file and extract gaps.

ofile = '/Users/leila/Documents/OOI_GitHub_repo/output_ric/CE04OSPS-SF01B-2A-CTDPFA107-streamed/tests/CE04OSPS-SF01B-2A-CTDPFA107-ctdpf_sbe43_sample-processed_on_2017-03-22T224100.csv'
out = open(ofile, 'w')
jfile = '/Users/leila/Documents/OOI_GitHub_repo/output_ric/CE04OSPS-SF01B-2A-CTDPFA107-streamed/tests/CE04OSPS-SF01B-2A-CTDPFA107-ctdpf_sbe43_sample-processed_on_2017-03-22T224100.json'
data = open(jfile).read()


particles = json.loads(data)
data_0 =['Level','Deployment','StartTime','EndTime','Annotation','Status','Redmine#','Todo','reviewed_by']
data_in = []
data_in.append(data_0)
cnt = 1

init = particles.keys()
print particles['ref_des']

col_index =-1
for listed in init:
    if 'deployments' in listed:
        init_result = particles[listed]
        for ii in range(len(init_result)):
            init_more = init_result[ii].keys()
            print listed, '-', ii+1, ': '
            print '   begin', '-', particles[listed][ii]['begin']
            print '   end', '-', particles[listed][ii]['end']
            for more_listed in init_more:
                if 'streams' in more_listed:
                    more_result = particles[listed][ii][more_listed]
                    for jj in range(len(more_result)):
                        more_more = more_result[jj].keys()
                        print '   stream_name', ':', particles[listed][ii][more_listed][0]['name']
                        for get_list in more_more:
                            if 'files' in get_list:
                                get_result= particles[listed][ii][more_listed][jj][get_list]
                                print '   number of files = ', ' ', len(get_result)
                                for nn in range(len(get_result)):
                                    n_gp_list = particles[listed][ii][more_listed][jj][get_list][nn]['time_gaps']
                                    n_gp_name = particles[listed][ii][more_listed][jj][get_list][nn]['name']
                                    if len(n_gp_list) is not 0:
                                        print n_gp_name

                                        for mm in range(len(n_gp_list)):
                                            print '   ', n_gp_list[mm]
                                            name = 'data_' + str(cnt)
                                            print name
                                            name = []

                                            name.append(particles['ref_des'])
                                            name.append(ii+1)
                                            name.append(n_gp_list[mm][0])
                                            name.append(n_gp_list[mm][1])
                                            name.append('')
                                            name.append('NOT_OPERATIONAL')
                                            name.append('')
                                            name.append('')
                                            name.append('leila')
                                            cnt += 1

                                            data_in.append(name)

print data_in

with open(ofile,'wb') as resultFile:
    wr = csv.writer(resultFile, dialect='excel')
    for row_index in range(len(data_in)):
        row = data_in[row_index]
        wr.writerow(row)
        #wr.writerow('\n')