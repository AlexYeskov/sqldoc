import os
import yaml

# import project settings

with open('./config/main_config.yaml') as config_file:
    settings = yaml.load(config_file)

# main function that takes the filename and returns HTML table

def parseSQLscript(filename,settings):

    output = ''

    create_flag = 0
    open_comment_flag = 0

    def get_col_name(line):
        if len(line.split('--')[0].lstrip().lstrip('\t').lstrip(',').split()) > 0:
            return line.split('--')[0].lstrip().lstrip('\t').lstrip(',').split()[0]
        else:
            return ''

    def get_comment(line):
        if '--' in line:
            return line.split('--')[1].strip()
        else:
            return ''

    def get_data_type(line):

        data_types = ['char', 'int', 'integer', 'numeric', 'float', 'date', 'timestamp', 'bool', 'boolean', 'text']
        if settings["db_engine"]=="Redshift":
            data_types = ['char', 'int', 'numeric', 'float', 'date', 'timestamp', 'bool', 'boolean']
        elements = line.split()
        for e in elements:
            if any(x in e for x in data_types) and '_' not in e:
                return e.replace("--", "").strip(' ').strip('\t')
        return ''

    def get_encoding(line):
        elements = line.split()
        for i in range(0, len(elements)):
            if 'encode' in elements[i]:
                return elements[i + 1].replace("--", "").strip()
        return ''

    # read the file

    with open(filename) as f:

        lines = f.readlines()
        index = 0

        for l in lines:

            index +=1

            if len(l)==1:

                continue

            if "CREATE TABLE" in l and '(' in l and any(x in l for x in settings["tables"]) and "audit" not in l and 'like' not in l:

                create_flag = 1

                table_name = l.replace("CREATE TABLE ","").replace(" (","").strip()

                print ("parsing DDL for {0}...".format(table_name))

                if settings["github_account"]!=None and settings["github_repo"]!=None:

                    script_path_elements = filename.strip("/").split("/")
                    if settings["github_repo"] in script_path_elements:
                        script_relative_path = "/".join(script_path_elements[script_path_elements.index(settings["github_repo"])+1:])
                    else:
                        script_relative_path = filename
                    table_name_subheader = ('<a href="https://github.com/{0}/{1}/tree/master/{2}#L{3}" target="_blank">{4}</a> ').format(settings["github_account"],settings["github_repo"],script_relative_path,index,table_name)

                else:

                    table_name_subheader = table_name

                output += ('\n<tr class="sqldocs-tablename" id="'+table_name+'"><td colspan="5">'+table_name_subheader+'</td></tr>')

            if create_flag==1 and (any(x in l for x in [';','DISTSTYLE','DISTKEY']) or l.strip()==')'):

                create_flag = 0
                continue

            if create_flag==1 and "CREATE TABLE" not in l:

                if '/*' in l and len(l.strip())>5:

                    open_comment_flag=1
                    output += ('\n<tr>')
                    output += ('\n<td class="sqldocs-select"></td>')
                    output += ('\n<td class="sqldocs-colname">'+get_col_name(l)+'</td>')
                    output += ('\n<td class="sqldocs-datatype">'+get_data_type(l)+'</td>')
                    if settings["db_engine"]=="Redshift":
                        output += ('\n<td class="sqldocs-encoding">'+get_encoding(l)+'</td>')
                    output += ('\n<td class="sqldocs-comment">')
                    continue

                if '*/' in l:

                    open_comment_flag=0
                    output += ('\n</td>\n</tr>')
                    continue

                if l.strip()[:2] == '--':

                    output += ('\n<tr class="sqldocs-section"><td colspan="5">' + l.replace('--', '').strip() + '</td></tr>')

                else:

                    if open_comment_flag==0:

                        output += ('\n<tr>')
                        output += ('\n<td class="sqldocs-select"><input type="checkbox" name="'+table_name+'"></td>')
                        output += ('\n<td class="sqldocs-colname">'+get_col_name(l)+'</td>')
                        output += ('\n<td class="sqldocs-datatype">'+get_data_type(l)+'</td>')
                        if settings["db_engine"] == "Redshift":
                            output += ('\n<td class="sqldocs-encoding">'+get_encoding(l)+'</td>')
                        output += ('\n<td class="sqldocs-comment">'+get_comment(l)+'</td>')
                        output += ('\n</tr>')

                    else:

                        output += ('<span class="sqldocs-comment">'+l+'</span>')

    return output

if __name__ == '__main__':

    input_path = settings["input_path"]

    results = []

    if os.path.isfile(input_path) and "sql" in input_path:
        results.append(parseSQLscript(input_path,settings))

    elif os.path.isdir(input_path):

        for filename in sorted(os.listdir(input_path)):
            if "sql" in filename:
                results.append(parseSQLscript(input_path+"/"+filename,settings))

    else:
        results = ["No file or folder detected at the specified path. Please verify the config file at ./config/main_config.yaml!"]

    doc_table = '\n'.join(results)

    # put together the final HTML pages

    with open('./config/catalog_template.html') as f:

        template = f.read()

        if settings["db_engine"]=="Redshift":

            template = template.replace('<!-- <th><div class="th-inner"><div>Encoding</div></div></th> -->','<th><div class="th-inner"><div>Encoding</div></div></th>')

        output_doc_contents = template.replace("<!-- HTML output of the doc parser -->",doc_table)

        output_file = open("./web/table_catalog.html", "w")
        output_file.write(output_doc_contents)