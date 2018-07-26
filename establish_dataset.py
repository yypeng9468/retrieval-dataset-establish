import os
import shutil
import uuid
from subprocess import call
import json
import argparse
import time


def make_upload_config(src_dir,bucket,key_prefix):
    d = {
        "src_dir":src_dir,
         "bucket":bucket,
         "key_prefix":key_prefix,
         "ignore_dir" : True,
         "log_file":"upload.log",
         "log_level": "info"
        }
    with open("upload.config", "w") as f:
        json.dump(d, f)

def parse_args():
    parser = argparse.ArgumentParser(description='set upload.config')
    # parser.add_argument('--ak', dest='access_key', help='access_key for qiniu account',
    #                     type=str)
    # parser.add_argument('--sk', dest='secret_key', help='secret_key for qiniu account',
    #                     type=str)
    parser.add_argument('--src_dir', dest='src_dir', help='images source directory',
                        type=str)
    # parser.add_argument('--bucket', dest='bucket', help='bucket to upload',
    #                     type=str)

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    access_key = "qNeBr5mvcSt3G8kM5M_icVKo65XtyY89tuaONzms"
    secret_key = "He7OlVlgKO-cNLbJt3Qp9G8OzJzA4BmT77yb3XyX"
    call(["qshell", "-m", "account", access_key, secret_key])

    """
    1.rename all your query images into 
    1.jpg, 2.jpg ...
    """
    root_query = os.getcwd()+"/query/"
    # n = 0
    # for q in os.listdir(root_query):
    #     if not q.endswith('DS_Store') and os.path.isfile(os.path.join(root_query, q)):
    #         src = os.getcwd()+"/query/"+q
    #         dst = os.getcwd()+"/query/{}.{}".format(n, q.split(".")[-1])
    #         shutil.move(src, dst)
    #         n+=1

    """
    2. establish a new file named image_retrieval
    and match query images and its n corresponding 
    images together
    """
    dir = args.src_dir
    # if not os.path.exists(dir):
    #     os.makedirs(dir)

    # num_queries = 10
    # for i in range(0,num_queries):
    #     if not os.path.exists(dir+"{}".format(str(i))):
    #         os.makedirs(dir+"{}".format(str(i)))

    for q in os.listdir(root_query):
        if not q.endswith('DS_Store') and os.path.isfile(os.path.join(root_query, q)):
            src = root_query+q
            dst = os.getcwd()+"/"+dir+q.split(".")[0]+"/query."+q.split(".")[-1]
            shutil.copyfile(src,dst)

    root_correspondence = os.getcwd()+"/correspondence/"
    for cor in os.listdir(root_correspondence):
        n = 0
        if not cor.endswith('DS_Store') and os.path.isdir(os.path.join(root_correspondence, cor)):
            for c in os.listdir(root_correspondence+cor):
                if not c.endswith('DS_Store') and os.path.isfile(os.path.join(root_correspondence,cor,c)):
                    src = root_correspondence+cor+"/"+c
                    dst = os.getcwd()+"/"+dir+cor+"/"+ "base_{}".format(n) +"."+c.split(".")[-1]
                    shutil.copyfile(src,dst)
                    n+=1
    re = []
    for im_ret in os.listdir(dir):
        j = 0
        dic = {}
        base = []
        if not im_ret.endswith('DS_Store') and os.path.isdir(os.path.join(dir, im_ret)):
            for im in os.listdir(dir+im_ret):
                if not im.endswith('DS_Store') and os.path.isfile(os.path.join(dir,im_ret,im)):
                    if im.split(".")[0]=="query":
                        src_q = os.getcwd()+"/"+dir+im_ret+"/"+im
                        dst_q = os.getcwd()+"/"+dir+im_ret+"/"+"query{}_".format(im_ret)+str(uuid.uuid4())+"."+im.split(".")[-1]
                        shutil.move(src_q,dst_q)
                    else:
                        src_b = os.getcwd()+"/"+dir+im_ret+"/"+im
                        dst_b = os.getcwd()+"/"+dir+im_ret+"/"+"base{}_{}_".format(im_ret,j)+str(uuid.uuid4())+"."+im.split(".")[-1]
                        base.append(dst_b.split("/")[-1])
                        shutil.move(src_b,dst_b)
                        j+=1
        dic["query"] = dst_q.split("/")[-1]
        dic["base"] = base
        re.append(dic)

    json_file = "result_{}.json".format(time.strftime("%Y%m%d-%H%M%S"))
    with open(json_file, "w") as r:
        json.dump(re, r, indent=4)

    for im_ret in os.listdir(dir):
        if not im_ret.endswith('DS_Store') and os.path.isdir(os.path.join(dir, im_ret)):
            for im in os.listdir(os.path.join(dir, im_ret)):
                if not im.endswith('DS_Store') and os.path.isfile(os.path.join(dir,im_ret,im)):
                    if im.split("_")[0][:5]=="query":
                        im_query = args.src_dir+"query/"
                        if not os.path.exists(im_query):
                            os.makedirs(im_query)
                        src = dir+im_ret+"/"+im
                        dst = im_query+im
                        shutil.copyfile(src,dst)
                    else:
                        im_base = args.src_dir+"base/"
                        if not os.path.exists(im_base):
                            os.makedirs(im_base)
                        src = dir+im_ret+"/"+im
                        dst = im_base+im
                        shutil.copyfile(src,dst)
    
    bucket = "retrieval-data-test-dataset"
    make_upload_config(im_query, bucket, "query/")
    call(["qshell", "-m", "qupload", "100", "upload.config"])
    time.sleep(5)
    make_upload_config(im_base, bucket, "base/")
    call(["qshell", "-m", "qupload", "100", "upload.config"])






