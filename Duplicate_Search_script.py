import sys
import os
import hashlib
import optparse

def main():
  def chunk_reader(fobj, chunk_size=1024):
      
      while True:
          chunk = fobj.read(chunk_size)
          if not chunk:
              return
          yield chunk

  def check_for_duplicates(paths, hashes, hash=hashlib.sha1):
         
          for dirpath, dirnames, filenames in os.walk(paths):
                for filename in filenames:
                   
                    full_path = os.path.join(dirpath, filename)
                    hashobj = hash()
                    for chunk in chunk_reader(open(full_path, 'rb')):
                        hashobj.update(chunk)
                    file_id = (hashobj.digest(), os.path.getsize(full_path))
                    duplicate = hashes.get(file_id, None)
                    if duplicate:
                        
                        print ("Duplicate found: %s and %s" % (full_path, duplicate))
                    else:
                        print ("File: %s" % (full_path))
                        hashes[file_id] = full_path
          return hashes

#---------------------------------------------------------------------------
  parser = optparse.OptionParser()

  parser.add_option('-i', '--input_dir', type=str,
        help="directory with files", default="./test_dir/")

  options, args = parser.parse_args()     

  if sys.argv[1:]:
    path=sys.argv[1:]
    with open(path[1]) as file:
        st = file.read().splitlines()
    hashes={}
    for catalog in st:
            print("Сatalog : ",catalog)
            hashes=check_for_duplicates(catalog,hashes)
    

  else:
      print("Please pass the paths to check as parameters to the script")

if __name__ == "__main__":
  main()
  
