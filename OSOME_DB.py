"""
OsomeDB 1.0.3
Author Merwin
Structure of DATA :
    DB - > Collections - > Docs - > DATA

Structure of Files :
    - > Folder(DB_NAME)
        - > File(Collection-1)
        - > File(Collection-2)
        - > File(Collection-3)
        - > Config.json
        - > PassBin-1(Created When There is a request for saving passwords)

Config File (json) :
    - > DB_NAME
    - > Date Created
    - > List of collections
    - > enc

    Eg : {"DB_NAME":"A","CREATED":"","COLLECTIONS":["A","B","C"],"ENC":false}
PassBin (json):
    Eg : {"Id":"Guy-1","Password":"The Guy's Password"}

Features :
 - > Enc
 - > Compression
 - > PassBin
"""


import os
import sty
import json
import zlib
import base64
import hashlib
import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC



class OsomeDB:
    def __init__(self,db_path):
        """
        If No DB exists in db_path a new one will bw created
        :param db_path: Path to the DB
        """
        self.db_path = db_path
        self.db_name = str(db_path).split("/")[-1]
        if os.path.exists(db_path):
            if os.path.isdir(db_path):
                self.renew_db()
                self.print_info("Renewing  DB")
            else:
                raise Exception("The DB is not a Dir")
        else:
            self.print_info("Making New DB")
            self.make_new_db()
        self.db_name = self.get_db_name()
        self.enc = self.get_settings()["ENC"]
        self.collections = self.get_db_collections()


    def __str__(self):
        return f"Name : {self.db_name} Collections : {self.collections} Doc-len : {self.total_docs()}"


    def __repr__(self):
        return  str({"Name" : self.db_name , "Collections" : self.collections,"Doc-len" : self.total_docs()})


    def __len__(self):
        return self.total_collections()


    def __int__(self):
        return self.total_collections()


    def __sizeof__(self):
        return self.get_db_size()


    def __bool__(self):
        return True


    def __iadd__(self, other):
        self.make_collection(other)


    def __isub__(self, other):
        try:
            self.remove_collection(other)
        except:
            raise Exception(f"Error : `{other}` Not found in the DB `{self.db_name}`")


    def collection_exists(self,collection):
        """
        Checks if a collection exists.
        :param collection: Name Of the Collection
        :return: True / False
        """
        past = os.getcwd()
        try:
            os.chdir(self.db_path)
        except:
            pass
        result = os.path.exists(collection)
        try:
            os.chdir(past)
        except:
            pass
        return result


    def make_collection(self,collection):
        """
        Makes a Collection
        :param collection: Name of the Collection
        :return: None
        """
        past = os.getcwd()
        try:
            os.chdir(self.db_path)
        except:
            pass
        settings = self.get_settings()
        if not collection in settings["collections"]:
            new_settings= self.get_settings()
            new_settings["collections"].append(collection)
            self.write_settings(new_settings)
            self.renew_db()
        try:
            os.chdir(past)
        except:
            pass


    def date_created(self):
        """
        The Date when the DB was Created
        :return: Date
        """
        date = self.get_settings()["CREATED"]
        return date


    def get_collection(self,collection):
        """
        Returns a Collection obj
        :param collection: The Name of the Collection
        :return: Collection
        """
        return Collection(self.db_path,collection)


    def remove_collection(self,collection):
        """
        Deletes a Collection
        :param collection:  Name of the collection
        :return: None
        """
        past = os.getcwd()
        try:
            os.chdir(self.db_path)
        except:
            pass
        self.write_settings(self.get_settings()["collections"].remove(collection))
        self.renew_db()
        try:
            os.chdir(past)
        except:
            pass


    def total_collections(self):
        """
        :return: The Total Count of Collections
        """
        return len(self.get_settings()["collections"])


    def total_docs(self):
        """
        :return: Returns Total Number of Docs in the DB
        """
        total_len = 0
        for e in self.collections:
            total_len += len(self.load_collection(e))
        return total_len


    def make_new_db(self):
        os.mkdir(self.db_path)
        past = os.getcwd()
        os.chdir(self.db_path)
        today = datetime.date.today()
        date = today.strftime("%d/%m/%Y")
        config_file = open("config.json","x")
        config_data = {"DB_NAME":self.db_name,"CREATED":date,"collections":[],"ENC":False}
        config_file.write(json.dumps(config_data))
        config_file.close()
        self.print_info("New Config File created")
        os.chdir(past)


    def get_db_name(self):
        """
        :return: The Name of the DB
        """
        return self.get_settings()["DB_NAME"]


    def get_db_size(self):
        """
        Gives the Size of the DB
        :return: Size
        """
        size = 0
        for path, dirs, files in os.walk(self.db_path):
            for f in files:
                fp = os.path.join(path, f)
                size += os.path.getsize(fp)
        return size


    def get_db_collections(self):
        """
        :return: Name of all the Collections
        """
        return self.get_settings()["collections"]


    def get_settings(self):
        """
        :return: The data in the Config File
        """
        past = os.getcwd()
        try:
            os.chdir(self.db_path)
        except:
            pass
        config_fle = open("config.json","r")
        data = config_fle.read()
        config_fle.close()
        try:
            os.chdir(past)
        except:
            pass
        return json.loads(data)


    def write_settings(self,settings):
        """
        ReWrites the Config File
        :param settings: New Settings
        :return: None
        """
        past = os.getcwd()
        try:
            os.chdir(self.db_path)
        except:
            pass
        config_fle = open("config.json", "w")
        config_fle.write(json.dumps(settings))
        config_fle.close()
        try:
            os.chdir(past)
        except:
            pass


    def renew_db(self):
        """
        Renews the DB with the new config file
        :return: None
        """
        if not os.getcwd() == self.db_path:
            past = os.getcwd()
            try:
                os.chdir(self.db_path)
            except:
                pass
            if not os.path.exists("config.json"):
                self.print_warning("Config file not found")
                today = datetime.date.today()
                date = today.strftime("%d/%m/%Y")
                config_file = open("config.json", "x")
                config_data = {"DB_NAME": self.db_name, "CREATED": date, "collections": [], "ENC": False}
                config_file.write(json.dumps(config_data))
                config_file.close()
                self.print_info("New Config File created")
            config = self.get_settings()
            for e in config["collections"]:
                if not os.path.exists(e):
                    file = open(e,"x")
                    file.write(json.dumps([]))
                    file.close()
            for e in os.listdir():
                if e not in config["collections"] and e != "config.json":
                    os.remove(e)
            try:
                os.chdir(past)
            except:
                pass
        else:
            if not os.path.exists("config.json"):
                self.print_warning("Config file not found")
                today = datetime.date.today()
                date = today.strftime("%d/%m/%Y")
                config_file = open("config.json", "x")
                config_data = {"DB_NAME": self.db_name, "CREATED": date, "collections": [],"ENC": False}
                config_file.write(json.dumps(config_data))
                config_file.close()
                self.print_info("New Config File created")
            config = self.get_settings()
            for e in config["collections"]:
                if not os.path.exists(e):
                    file = open(e, "x")
                    file.write(json.dumps([]))
                    file.close()
            for e in os.listdir():
                if e not in config["collections"] and e != "config.json":
                    os.remove(e)


    def load_collection_raw(self,collection):
        """
        Loads the raw collection data
        :param collection: Collection name
        :return: Raw Collection
        """
        try:
            past = os.getcwd()
            try:
                os.chdir(self.db_path)
            except:
                pass
            db_file = open(collection,"rb")
            raw_data = db_file.read()
            db_file.close()
            raw_data = self.de_compress(raw_data)
            if self.enc != False:
                try:
                    enc_ = Fernet(self.password_to_key(self.enc))
                    raw_data = enc_.decrypt(raw_data).decode()
                except:
                    pass
            try:
                os.chdir(past)
            except:
                pass
            return raw_data
        except:
            raise Exception("Error While Reading Collection")


    def load_collection(self,collection):
        """
        Returns the Collection data
        :param collection: Collection Name
        :return: Collection Data
        """
        try:
            return json.loads(self.load_collection_raw(collection))
        except:
            raise Exception("Error While Loading Collection")


    def write_collection_raw(self,collection,data):
        """
        Writes Raw collection data
        :param collection: Collection Name
        :param data: New Collection Data
        :return: None
        """
        try:
            past = os.getcwd()
            try:
                os.chdir(self.db_path)
            except:
                pass
            data = data.encode()
            if self.enc != False:
                enc_ = Fernet(self.password_to_key(self.enc))
                data = enc_.encrypt(data)
            data = self.compress(data)
            db_file = open(collection, "wb")
            db_file.write(data)
            db_file.close()
            try:
                os.chdir(past)
            except:
                pass
        except:
            raise Exception("Error While Writing Collection")


    def write_collection(self,collection,data):
        """
        Writes collection data
        :param collection: Collection Name
        :param data: New Collection
        :return: None
        """
        try:
            self.write_collection_raw(collection,json.dumps(data))
        except:
            raise Exception("Error While Saving Collection")


    def delete_collection(self,collection):
        """
        Deletes a Collection
        :param collection: Collection Name
        :return: None
        """
        try:
            past = os.getcwd()
            try:
                os.chdir(self.db_path)
            except:
                pass
            os.remove(collection)
            try:
                os.chdir(past)
            except:
                pass
        except:
            raise Exception("Error : Error While Deleting The Collection")


    def get_collection_size(self,collection):
        """
        Gets the size of the Collection
        :param collection: Collection Name
        :return: Size
        """
        try:
            past = os.getcwd()
            try:
                os.chdir(self.db_path)
            except:
                pass
            size = os.path.getsize(collection)
            try:
                os.chdir(past)
            except:
                pass
        except:
            raise Exception("Error : Error While Getting The Collection Size")
        return size


    def password_to_key(self,password):
        salt = b'.-Kh)ura/)\xcef\xc8\x88u\xc2'
        password = password.encode()
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key


    def compress(self,data):
        data_ = zlib.compress(data)
        if len(data_) < len(data):
            final = data_
        else:
            final = data
        return final


    def de_compress(self,data):
        try:
            data_ = zlib.decompress(data)
            return data_
        except:
            return data


    def print_info(self, data):
        print(f"{sty.fg(28, 178, 232)}INFO : {data}{sty.fg.rs}")


    def print_warning(self, data):
        print(f"{sty.fg(242, 74, 68)}WARNING : {data}{sty.fg.rs}")


    class PassBin:
        def __init__(self, db_path, bin_name):
            """
            :param db_path: Path to the DB
            :param bin_name: Name of the passbin
            """
            self.bin_name = bin_name
            self.db_path = db_path
            self.oosome = OsomeDB(self.db_path)
            if not self.oosome.collection_exists(bin_name):
                self.print_warning("PASSBIN NOT FOUND")
                self.make_new_passbin()


        def print_info(self, data):
            print(f"{sty.fg(28, 178, 232)}INFO : {data}{sty.fg.rs}")


        def print_warning(self, data):
            print(f"{sty.fg(242, 74, 68)}WARNING : {data}{sty.fg.rs}")


        def passbin_exists(self,bin_name):
            """
            Shows if a PassBin exists
            :param bin_name: Name of the passbin
            :return: True / False
            """
            result = os.path.exists(f"{self.db_path}/{bin_name}")
            return result


        def make_new_passbin(self):
            self.print_info(F"PASSBIN {self.bin_name} MADE")
            self.oosome.make_collection(self.bin_name)


        def get_pass_bin(self):
            """
            :return: The passbin
            """
            try:
                bin = self.oosome.load_collection(self.bin_name)
                return bin
            except:
                raise Exception("Error While Reading PassBin")


        def write_pass_bin(self,data):
            """
            Rewrite the passbin
            :param data: New PASSBIN DATA
            :return: None
            """
            try:
               self.oosome.write_collection(self.bin_name,data)
            except:
                raise Exception("Error While Writing PassBin")


        def __len__(self):
            return len(self.get_pass_bin())


        def __str__(self):
            return f"Name : {self.bin_name}"


        def __repr__(self):
            return f"Name : {self.bin_name} Len : {len(self.get_pass_bin())}"


        def __add__(self, other):
            new_collection = self.get_pass_bin()
            new_collection.append(other)
            return new_collection


        def __sub__(self, other):
            try:
                new_collection = self.get_pass_bin()
                new_collection.remove(other)
                return new_collection
            except:
                raise Exception(f"Error : `{other}` Not found in the PassBin `{self.bin_name}`")


        def __iadd__(self, other):
            new_pass_bin = self.get_pass_bin()
            new_pass_bin.append(other)
            self.write_pass_bin(new_pass_bin)
            return OsomeDB.PassBin(self.db_path, self.bin_name)


        def __isub__(self, other):
            try:
                pass_bin  = self.get_pass_bin()
                pass_bin.remove(other)
                self.write_pass_bin(pass_bin)
                return OsomeDB.PassBin(self.db_path, self.bin_name)
            except:
                raise Exception(f"Error : `{other}` Not found in the PassBin `{self.bin_name}`")


        def __int__(self):
            return len(self.get_pass_bin())


        def delete_bin(self):
            """
            Deletes the PassBin
            :return: None
            """
            self.oosome.delete_collection(self.bin_name)
            self.print_info(F"PASSBIN {self.bin_name} DELETED")


        def __bool__(self):
            return True


        def get_passbin_size(self,bin_name):
            """
            Give the size of the passbin
            :param bin_name: PassBin Name
            :return: Size
            """
            try:
                past = os.getcwd()
                try:
                    os.chdir(self.db_path)
                except:
                    pass
                size = os.path.getsize(bin_name)
                try:
                    os.chdir(past)
                except:
                    pass
            except:
                raise Exception("Error : Error While Getting The PassBin's Size")
            return size


        def __sizeof__(self):
            return self.get_passbin_size(self.bin_name)


        def append_new_pass(self, Id, Password):
            """
            Appends New Password
            :param Id: Id of the Password
            :param Password: Password
            :return: None
            """
            col_data = self.get_pass_bin()
            col_data.append({"Id":Id,"Password":self.custom_hash(Password)})
            self.write_pass_bin(col_data)


        def remove(self,Id):
            """
            Removes a password form PassBin which have the provided Id
            :param Id: Id of the Password
            :return: None
            """
            try:
                pass_bin = self.get_pass_bin()
                pass_bin.remove(self.search_by_Id(Id[1]))
                self.write_pass_bin(pass_bin)
            except:
                raise Exception(f"Error : `{Id}` Not found in the PassBin `{self.bin_name}`")


        def reset_pass(self, Id, Password):
            """
            Reset a Password By Given Id
            :param Id: Id of the Password
            :param Password: New Password
            :return: None
            """
            col_data = self.get_pass_bin()
            elem = self.search_by_Id(Id)
            col_data[elem[0]] = {"Id":Id,"Password":self.custom_hash(Password)}
            self.write_pass_bin(col_data)


        def custom_hash(self,data):
            result = hashlib.sha256(data.encode())
            result = result.hexdigest()
            return result


        def search_by_Id(self,Id):
            """
            Search a Password By Id
            :param Id: Id of the password
            :return: Index , Item
            """
            col_data = self.get_pass_bin()
            for e in col_data:
                if e["Id"] == Id:
                    return (col_data.index(e), e)


    class Settings:
        def __init__(self,db_path):
            """
            :param db_path: The path to the DB
            """
            self.db_path = db_path


        def change(self,key,value):
            """
            Change The VALUE of a key in config.json
            :param key: Key
            :param value: New Value
            :return: None
            """
            settings = self.get_settings()
            settings[key]=value
            self.write_settings(settings)


        def give_setting_info(self):
            """
            Gives Info about what all setting are available
            :return: Info
            """
            info = """
    Config File (json) :
    - > DB_NAME
    - > Date Created
    - > List of collections
    - > enc
    - > compression
            """
            return info


        def get(self,key):
            """
            Get the value of a Key
            :param key: Key
            :return: Value
            """
            return self.get_settings()[key]


        def get_settings(self):
            """
            Loads the settings
            :return: Settings
            """
            past = os.getcwd()
            try:
                os.chdir(self.db_path)
            except:
                pass
            config_fle = open("config.json", "r")
            data = config_fle.read()
            config_fle.close()
            try:
                os.chdir(past)
            except:
                pass
            return json.loads(data)


        def write_settings(self, settings):
            """
            Rewrites the settings
            :param settings: New Settings
            :return: None
            """
            past = os.getcwd()
            try:
                os.chdir(self.db_path)
            except:
                pass
            config_fle = open("config.json", "w")
            config_fle.write(json.dumps(settings))
            config_fle.close()
            try:
                os.chdir(past)
            except:
                pass


class Collection(OsomeDB):
    def __init__(self,db_path,collection):
        """
        :param db_path: Path to the DB
        :param collection: Name of the Collection
        """
        super().__init__(db_path)
        self.collection_name = collection


    def __len__(self):
        return len(self.load_collection(self.collection_name))


    def __str__(self):
        return f"Name : {self.collection_name}"


    def __repr__(self):
        return f"Name : {self.collection_name} Len : {len(self.load_collection(self.collection_name))}"


    def __add__(self, other):
        new_collection = self.read_collection_data()
        new_collection.append(other)
        return new_collection


    def __sub__(self, other):
        try:
            new_collection = self.read_collection_data()
            new_collection.remove(other)
            return new_collection
        except:
            raise Exception(f"Error : `{other}` Not found in the Collection `{self.collection_name}`")


    def __iadd__(self, other):
        new_collection = self.read_collection_data()
        new_collection.append(other)
        self.rewrite_collection_data(new_collection)
        return Collection(self.db_path,self.collection_name)


    def __isub__(self, other):
        try:
            new_collection = self.read_collection_data()
            new_collection.remove(other)
            self.rewrite_collection_data(new_collection)
            return Collection(self.db_path,self.collection_name)
        except:
            raise Exception(f"Error : `{other}` Not found in the Collection `{self.collection_name}`")


    def __int__(self):
        return len(self.load_collection(self.collection_name))


    def delete(self):
        self.delete_collection(self.collection_name)


    def __bool__(self):
        return True


    def __sizeof__(self):
        return self.get_collection_size(self.collection_name)


    def read_collection_data(self):
        """
        Gives the collection data
        :return: Collection Data
        """
        return self.load_collection(self.collection_name)


    def rewrite_collection_data(self,data):
        """
        Rewrites the Collection
        :param data: New Data
        :return: None
        """
        self.write_collection(self.collection_name,data)


    def get_indexof(self,data):
        """
        Get The index of a given doc
        :param data: Doc's data
        :return: Index
        """
        return self.read_collection_data().index(data)


    def get_byindex(self,index):
        """
        Gets a Doc By Index
        :param index: Index
        :return: Doc
        """
        return self.read_collection_data()[index]


    def search_by_key_val(self,key_name,val):
        """
        Search using the value of a given key
        :param key_name: Name of the key
        :param val: Value
        :return: Index , Doc
        """
        col_data = self.read_collection_data()
        for e in col_data:
            if e[key_name] == val:
                return (col_data.index(e),e)


    def rewrite_doc(self,index,new_data):
        """
        Rewrites a doc with given Index
        :param index: Index
        :param new_data: New Doc Data
        :return: None
        """
        col_data = self.read_collection_data()
        col_data[index] = new_data
        self.rewrite_collection_data(col_data)

