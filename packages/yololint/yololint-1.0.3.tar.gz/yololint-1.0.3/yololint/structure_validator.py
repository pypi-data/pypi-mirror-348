import os
import yaml
from yololint.utils.compare_validate import compare_validate
from yololint.utils.add_file_to_list import add_file_to_list
from yololint.constants.folders import BASIC_FOLDERS, CHILD_FOLDERS

class StructureValidator:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.__errors = []

    def dataset_validation(self):

        if not os.path.exists(self.dataset_path):
            self.__errors.append("🚫 Dataset path doesn't exist or is incorrect! 📁")
            return self.__errors
        basic_subfolders = []
        data_yaml = ''
        for basic_subfolder in os.listdir(self.dataset_path):
            if basic_subfolder.endswith('.yaml'):
                data_yaml = basic_subfolder
            else: basic_subfolders.append(basic_subfolder)
         
         
        basic_compare_valid = compare_validate(basic_subfolders, BASIC_FOLDERS)
        if basic_compare_valid:
            self.__errors.append("📂 Missing required base folders! Expected but not found: " + ", ".join(basic_compare_valid))
            return self.__errors
  
        if data_yaml == '':
            self.__errors.append(f"❌ Missing required file: `data.yaml` 🧾")
            return self.__errors
        
        with open(os.path.join(self.dataset_path, data_yaml), 'r') as f:
            data_config = yaml.safe_load(f)
            if not data_config:
                self.__errors.append("⚠️ Your `data.yaml` file is empty or invalid! ❗")
                return self.__errors
            if not data_config.get('names'):
                self.__errors.append("🔍 Missing `names` field in your `data.yaml` file. Please define class names. 🧠")
                return self.__errors
            class_names = data_config.get('names')
            if not data_config.get('nc'):
                self.__errors.append("🔍 Missing `nc` field (number of classes) in your `data.yaml` file. 🧮")
                return self.__errors
            num_classes = data_config.get('nc')
            if not len(class_names) == num_classes:
                self.__errors.append("❌ The number of class names does not match `nc`. Check your `data.yaml`! 🔢")
                return self.__errors
        
        child_subfolders = []
 
        for folder in BASIC_FOLDERS:

            child_folder_path = os.path.join(self.dataset_path, folder)
           
            for child_folder in os.listdir(child_folder_path):
                child_subfolders.append(child_folder)

       
            child_compare_valid = compare_validate(child_subfolders, CHILD_FOLDERS)
            if  child_compare_valid:
                self.__errors.append(f"📁 Missing child folders in `{folder}`. Expected: {', '.join(child_compare_valid)} 📂")
                return self.__errors
            child_subfolders = []
  
      
        len_train_images = len(add_file_to_list(os.path.join(self.dataset_path, 'images/train')))
        len_test_images = len(add_file_to_list(os.path.join(self.dataset_path, 'images/val')))
        len_train_txt = len(add_file_to_list(os.path.join(self.dataset_path, 'labels/train')))
        len_test_txt = len(add_file_to_list(os.path.join(self.dataset_path, 'labels/val')))


        if (len_train_images != len_train_txt or len_train_images < 0 or len_train_txt < 0) or (len_test_images != len_test_txt or len_test_images < 0 or len_test_txt < 0):
            self.__errors.append(f"🖼️ Number of images and annotation files (.txt) doesn't match!\n"
    f"Train Images: {len_train_images}, Train Labels: {len_train_txt}\n"
    f"Val Images: {len_test_images}, Val Labels: {len_test_txt} ⚠️")
            return self.__errors

        return f"🧪 Validation complete.\n❗ Errors found:\n" + "\n".join(self.__errors) if self.__errors else "✅ All checks passed. Dataset structure looks good! 🧼"
        