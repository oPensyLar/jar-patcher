import glob
import zipfile
import os
from pathlib import Path
import shutil


find_dir = ["/root", "/mnt"]
output_dir = "/tmp/jar_output/"
target_class = ["JMSAppender.class", "JndiLookup.class"]
file_log = "/tmp/log4j_vuln_upgrade.log"


def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            prm1 = os.path.join(root, file)
            prm2 = os.path.relpath(os.path.join(root, file), path)
            ziph.write(prm1, prm2)


def check_jar(file_path, output_tmp_folder, class_to_remove, handle):
    output_str = ""

    try:
        with zipfile.ZipFile(file_path, 'r') as zip_file:
            for c_file in zip_file.infolist():
                # output_str = output_str + "list files " + c_file.filename + "\n"
                for c_class in class_to_remove:
                    if c_file.filename.find(c_class) > 0x0:
                        output_str = output_str + "[+] Found " + c_class + " on " + file_path + "\n"

                        # create dir
                        filename = Path(file_path).stem
                        final_dir = output_tmp_folder + "/" + filename + "/"
                        os.mkdir(final_dir)

                        # create dir and copy original .jar
                        original_jar_dir = final_dir + "original"
                        os.mkdir(original_jar_dir)
                        base_name = os.path.basename(file_path)
                        original_jar_dir_with_ext = original_jar_dir + "/" + base_name
                        shutil.copyfile(file_path, original_jar_dir_with_ext)

                        # create dir
                        original_jar_mod_dir = final_dir + "mod"
                        os.mkdir(original_jar_mod_dir)

                        # create dir
                        original_jar_mod_unzip_dir = original_jar_mod_dir + "/unzip"
                        os.mkdir(original_jar_mod_unzip_dir)

                        # create dir
                        original_jar_new_jar_dir = original_jar_mod_dir + "/new_jar"
                        os.mkdir(original_jar_new_jar_dir)
                        jar_patched_file_name = original_jar_new_jar_dir + "/" + base_name

                        # find vuln .class
                        zip_file.extractall(original_jar_mod_unzip_dir)
                        dir_find = original_jar_mod_unzip_dir + "/**/" + c_class
                        class_found = glob.glob(dir_find, recursive=True)

                        # remove vuln .class
                        for file_to_delete in class_found:
                            output_str = output_str + "[+] Removing " + file_to_delete + "\n"
                            os.remove(file_to_delete)

                        # create zip/jar
                        new_jar = zipfile.ZipFile(jar_patched_file_name, 'w', zipfile.ZIP_DEFLATED)
                        zipdir(original_jar_mod_unzip_dir, new_jar)
                        new_jar.close()

                        # hot patching
                        output_str = output_str + "[+] Replacing " + file_path + " with " + jar_patched_file_name + "\n"
                        shutil.copy(jar_patched_file_name, file_path)

#    except FileNotFoundError:
#        output_str = "[!] FileNotFoundError on " + file_path + "\n"

    except zipfile.BadZipFile:
        output_str = "[!] BadZipFile on " + file_path + "\n"

    return output_str


def deploy(path_to_find, path_to_output, t_class):
    output_str = ""
    handle_log = open(file_log, "w")

    for c_dir in path_to_find:
        files = glob.glob(c_dir + "/**/*.jar", recursive=True)

        output_str = output_str + "Total jars found " + str(len(files)) + " over " + c_dir + "\n"

        if os.path.exists(output_dir) is False:
            os.mkdir(output_dir)

        i = 0x0
        for c_file in files:
            output_str = output_str + "Checking " + c_file + " (" + str(i) + ")" + "\n"
            output_str = output_str + check_jar(c_file, path_to_output, t_class, handle_log)
            i += 1

    output_str = output_str + "[+] Script completed!\n"
    handle_log.write(output_str)
    handle_log.close()


deploy(find_dir, output_dir, target_class)