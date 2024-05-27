import os
import hashlib
import logging
import shutil
import time

global log_file
def synchronize_folders(source_path, replica_path, log_file):

  if is_file(log_file):
    logfile = os.path.join(log_file)
  else:
    logfile = os.path.join(log_file,"logs.txt")

  try:
      logging.basicConfig(filename=logfile, level=logging.INFO,format='%(asctime)s %(message)s')
  except PermissionError as e:
    print(f"Error: Permission denied: {log_file}")

  # Create replica directory if it doesn't exist
  if not path_exist(replica_path):
    os.makedirs(replica_path)
    log_message(f"Created replica folder: {replica_path}")

  # Loop through all files and subdirectories in the source folder
  for root, dirs, files in os.walk(source_path):
    relpath = os.path.relpath(root, source_path)
    replica_dir = os.path.join(replica_path, relpath)

    # Remove extra files/folders in replica that don't exist in source
    for item in os.listdir(replica_dir):
      item_path = os.path.join(replica_dir, item)
      if not path_exist(os.path.join(root, item)):
        if is_file(item_path):
          os.remove(item_path)
          log_message(f"Removed extra file: {item_path}")
        else:
          shutil.rmtree(item_path)
          log_message(f"Removed extra directory: {item_path}")

    # Copy/Update files in replica based on source
    for filename in files:
      source_file = os.path.join(root, filename)
      replica_file = os.path.join(replica_dir, filename)

      # Check if file exists in replica and needs update
      if path_exist(replica_file):
        source_hash = get_file_hash(source_file)
        replica_hash = get_file_hash(replica_file)
        if source_hash != replica_hash:
          shutil.copy2(source_file, replica_file)
          log_message(f"Updated file: {replica_file}")
      else:
        shutil.copy2(source_file, replica_file)
        log_message(f"Copied file: {replica_file}")


def get_file_hash(file_path):
  with open(file_path, 'rb') as f:
    hasher = hashlib.md5()
    hasher.update(f.read())
    return hasher.hexdigest()


def log_message(message):
  try:
    logging.info(message)
    print(message)
  except PermissionError as e:
    print(f"Error: Permission denied: {log_file}")


def path_validation(path):
  return os.path.isdir(path)

def is_file(path):
  return os.path.isfile(path)

def is_int(value):
  return value.isdigit() and int(value) > 0

def path_exist(path):
  return os.path.exists(path)


if __name__ == "__main__":
  var_source_fold = var_repl_fold = var_log_fold = var_interval = ""

  while not path_validation(var_source_fold):
    var_source_fold = input(f"Path to the source folder:\n")


  var_repl_fold = input(f"Path to the replica folder:\n")

  while not path_validation(var_log_fold):
    var_log_fold = input("Path to the log folder:\n")


  while not is_int(var_interval):
    var_interval = input(f"Synchronization interval in seconds:\n")


  while True:
    synchronize_folders(var_source_fold, var_repl_fold, var_log_fold)
    time.sleep(int(var_interval))


