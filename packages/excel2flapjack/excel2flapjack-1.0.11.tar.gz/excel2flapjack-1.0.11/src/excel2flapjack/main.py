import os
import pandas as pd
from flapjack import Flapjack

class X2F:

    """ 
        inputData retrives information from input XDC excel template, connects to fj, and formats and uploads data
        includes: 
            - class definition
            - initialization method
            - class attributes
            - instance attributes
            - methods
        

        Instance Attributes
        ----------
        fj : flapjack.flapjack.Flapjack object
            fj case that contains the connection to fj account

        excel_path: path
            path to XDC spreadsheet

        df : pandas dataframe  
            contains all the information from XDC file in a format that can be used by FJ

        hash_map: dictionary
            key: name of study attributes from XDC spreadsheet
            value: corresponding flapjackID  

        fj_conv_sht: dataframe
            dataframe containing information from XDC spreadsheet FJ conversion page
            - Sheet name: name of sheet containing rest of info
            - ColName: name of column on 'Sheet name' containing XDC data
            - FlapjackName: name of flapjack object corresponding to respective XDC data

        sbol_hash_map: dictionary
            key: index of flapjack id
            value: sbol uri

    """
    # list of all the sheet names in XDC excel file
    # each will define an fj object with data extracted from the excel sheet
    # use self.types to access this class attribute
    

    def __init__(self, 
                 excel_path:str, 
                 fj_url:str, 
                 sbol_hash_map:dict = None,
                 confirm:bool = False,
                 overwrite:bool = False
                 ):
        # fj url has to include 8000 port # this is when the port is not directed properly
        #if not fj_url.endswith(":8000"):
        #    fj_url = fj_url + ":8000"

        self.fj = Flapjack(url_base=fj_url)
        # for testing log_in, no login just returns None
        # create a new method for this so we can call it and make sure we're logged in before running the rest of everything
        # self.fj.log_in(username = fj_user, password = fj_pass)

        # convert excel path to pd.Excel File and parse
        self.fj_url = fj_url
        self.confirm = confirm
        self.overwrite = overwrite
        self.xls = pd.ExcelFile(excel_path)
        self.fj_conv_sht = self.xls.parse('FlapjackCols', skiprows=0)
        self.df = pd.DataFrame()
        self.hash_map = {}
        self.del_map = {}
        self.index_skiprows = 0
        self.sbol_hash_map = sbol_hash_map 
        self.sheet_object_hash_map = {'Chemical':'Chemical', 'DNA':'DNA', 'Supplement':'Supplement', 
                                        'Vector':'Vector', 'Strain':'Strain', 'Media':'Media' ,
                                        'Signal':'Signal', 'Study':'Study', 'Assay':'Assay',
                                        'Sample':'Sample', 'Measurement':'Measurement',
                                        'Sample Design':'Sample Design'}
        


    def print_info(self, fj_sht = False, df=False, hash_map=False):
        if fj_sht:
            print(self.fj_conv_sht)
        if df:
            print(self.df.head())
            print(self.df.info())
        if hash_map:
            print(self.hash_map)

    def generate_sheets_to_object_mapping(self):
        """
        Generates a dictionary with Key = sheet name and Value = Flapjack Object, extracting unique values.
        """
        #read flapjackcols sheet 
        fj_cols_df = self.xls.parse('FlapjackCols', skiprows=0)
        fj_cols_df = fj_cols_df.dropna()
        hash_map_sheet_name_to_fj_obj = {}
        for index, row in fj_cols_df.iterrows():
            #check if the key is already in the dictionary
            if row['Sheet Name'] not in hash_map_sheet_name_to_fj_obj:
                #if not, create a new list for that key
                hash_map_sheet_name_to_fj_obj[row['Sheet Name']] = row['FlapjackObject']
            else:
                #if it is, check if the value is the same as the existing one
                if hash_map_sheet_name_to_fj_obj[row['Sheet Name']] != row['FlapjackObject']:
                    #raise a warning if the value is different
                    print(f"Warning: {row['Sheet Name']} has multiple FlapjackObjects: {hash_map_sheet_name_to_fj_obj[row['Sheet Name']]} and {row['FlapjackObject']}")
                else:
                    #if it is, do nothing
                    pass
        self.sheet_object_hash_map = hash_map_sheet_name_to_fj_obj
        return self.sheet_object_hash_map
    

    def create_df(self):

        for sheet_name, fj_object_name in self.sheet_object_hash_map.items():
            # read in the conversion sheet for xdc col name to flapjack name 
                # for current obj
            fj_conv_sht_obj = self.fj_conv_sht.loc[(self.fj_conv_sht['Sheet Name'] == sheet_name)]
            fj_conv_sht_obj = fj_conv_sht_obj.set_index('ColName').to_dict('index')

            # read in current obj sheet
            obj_df = self.xls.parse(sheet_name, skiprows=self.index_skiprows, index_col=f'{fj_object_name} ID')
            cols = list(obj_df.columns)

            # drop cols not used by fj and rename ones that are
            new_cols = []
            drop_cols = []
            for col in cols:
                if col in fj_conv_sht_obj.keys():
                    new_cols.append(fj_conv_sht_obj[col]['FlapjackName'])
                else:
                    drop_cols.append(col)
            
            obj_df = obj_df.drop(columns=drop_cols)
            obj_df.columns = new_cols
            obj_df['object'] = fj_object_name
            obj_df['flapjackid'] = ''
            if self.sbol_hash_map is not None:
                # add a column to the revamp_df for sbol_uri
                obj_df['sbol_uri'] = ''
                # add sbol_uri to every row that has the same index as the key in sbol_hash_map
                for key, value in self.sbol_hash_map.items():
                    obj_df.loc[key, 'sbol_uri'] = value

            self.df = pd.concat([self.df,obj_df])#,ignore_index=True) #self.df.append(obj_df)

    
    def upload_studies(self):
        del_inds = []
        for index, row in self.df[self.df['object'] == 'Study'].iterrows():
            fj_obj = self.fj.create(
                'study',
                name=row['name'],
                description=row['description'],
                confirm=self.confirm,
                overwrite=self.overwrite,
            )
            for i in fj_obj:
                print(i, fj_obj[i][0])
            print()
            self.hash_map[index] = fj_obj.id[0]
            if fj_obj.id[0] not in del_inds:
                del_inds.append(fj_obj.id[0])
            self.df.loc[index, 'flapjackid'] = fj_obj.id[0]
            # if row[DOI] is not nan patch the DOI
            if not pd.isna(row['DOI']):
                self.fj.patch('study', fj_obj.id[0], doi=row['DOI'])
            # if index in sbol_hash_map patch the sbol uri
            if index in self.sbol_hash_map:
                self.fj.patch('study', fj_obj.id[0], sbol=self.sbol_hash_map[index])
        self.del_map['study'] = del_inds


    def upload_signals(self):
        del_inds = []
        for index, row in self.df[self.df['object'] == 'Signal'].iterrows():
            fj_obj = self.fj.create(
                'signal',
                name=row['name'],
                description=row['description'],
                color=row['color'],
                confirm=self.confirm,
                overwrite=self.overwrite,
            )
            for i in fj_obj:
                print(i, fj_obj[i][0])
            print()
            self.hash_map[index] = fj_obj.id[0]
            if fj_obj.id[0] not in del_inds:
                del_inds.append(fj_obj.id[0])
            # if index in sbol_hash_map patch the sbol uri
            if index in self.sbol_hash_map:
                self.fj.patch('signal', fj_obj.id[0], sbol=self.sbol_hash_map[index])
            self.df.loc[index, 'flapjackid'] = fj_obj.id[0]
        self.del_map['signal'] = del_inds


    def upload_chemicals(self):
        del_inds = []
        for index, row in self.df[self.df['object'] == 'Chemical'].iterrows():
            fj_obj = self.fj.create(
                'chemical',
                name=row['name'],
                description=row['description'],
                confirm=self.confirm,
                overwrite=self.overwrite,
            )
            for i in fj_obj:
                print(i, fj_obj[i][0])
            print()
            self.hash_map[index] = fj_obj.id[0]
            if fj_obj.id[0] not in del_inds:
                del_inds.append(fj_obj.id[0])
            # if index in sbol_hash_map patch the sbol uri
            if index in self.sbol_hash_map:
                self.fj.patch('chemical', fj_obj.id[0], sbol=self.sbol_hash_map[index])
            self.df.loc[index, 'flapjackid'] = fj_obj.id[0]
        self.del_map['chemical'] = del_inds

    def upload_dna(self):
        del_inds = []
        for index, row in self.df[self.df['object'] == 'DNA'].iterrows():
            fj_obj = self.fj.create(
                'dna',
                name=row['name'],
                confirm=self.confirm,
                overwrite=self.overwrite,
            )
            for i in fj_obj:
                print(i, fj_obj[i][0])
            print()
            self.hash_map[index] = fj_obj.id[0]
            if fj_obj.id[0] not in del_inds:
                del_inds.append(fj_obj.id[0])
            # if index in sbol_hash_map patch the sbol uri
            if index in self.sbol_hash_map:
                self.fj.patch('dna', fj_obj.id[0], sbol=self.sbol_hash_map[index])
            self.df.loc[index, 'flapjackid'] = fj_obj.id[0]
        self.del_map['dna'] = del_inds

    
    def upload_medias(self):
        del_inds = []
        for index, row in self.df[self.df['object'] == 'Media'].iterrows():
            fj_obj = self.fj.create(
                'media',
                name=row['name'],
                description=row['description'],
                confirm=self.confirm,
                overwrite=self.overwrite,
            )
            for i in fj_obj:
                print(i, fj_obj[i][0])
            print()
            self.hash_map[index] = fj_obj.id[0]
            if fj_obj.id[0] not in del_inds:
                del_inds.append(fj_obj.id[0])
            # if index in sbol_hash_map patch the sbol uri
            if index in self.sbol_hash_map:
                self.fj.patch('media', fj_obj.id[0], sbol=self.sbol_hash_map[index])
            self.df.loc[index, 'flapjackid'] = fj_obj.id[0]
        self.del_map['media'] = del_inds


    def upload_strains(self):
        del_inds = []
        for index, row in self.df[self.df['object'] == 'Strain'].iterrows():
            fj_obj = self.fj.create(
                'strain',
                name=row['name'],
                description=row['description'],
                confirm=self.confirm,
                overwrite=self.overwrite,
            )
            for i in fj_obj:
                print(i, fj_obj[i][0])
            print()
            self.hash_map[index] = fj_obj.id[0]
            if fj_obj.id[0] not in del_inds:
                del_inds.append(fj_obj.id[0])
            # if index in sbol_hash_map patch the sbol uri
            if index in self.sbol_hash_map:
                self.fj.patch('strain', fj_obj.id[0], sbol=self.sbol_hash_map[index])
            self.df.loc[index, 'flapjackid'] = fj_obj.id[0]
        self.del_map['strain'] = del_inds


    def upload_supplements(self):
        del_inds = []
        for index, row in self.df[self.df['object'] == 'Supplement'].iterrows():
            fj_obj = self.fj.create(
                'supplement',
                name=row['name'],
                description=row['description'],
                chemical=self.df.loc[row['chemical'], 'flapjackid'],
                concentration=row['concentration'],
                confirm=self.confirm,
                overwrite=self.overwrite,
            )
            for i in fj_obj:
                print(i, fj_obj[i][0])
            print()
            self.hash_map[index] = fj_obj.id[0]
            if fj_obj.id[0] not in del_inds:
                del_inds.append(fj_obj.id[0])
            # if index in sbol_hash_map patch the sbol uri
            if index in self.sbol_hash_map:
                self.fj.patch('supplement', fj_obj.id[0], sbol=self.sbol_hash_map[index])
            self.df.loc[index, 'flapjackid'] = fj_obj.id[0]
        self.del_map['supplement'] = del_inds


    def upload_vectors(self):
        del_inds = []
        for index, row in self.df[self.df['object'] == 'Vector'].iterrows():
            # print(self.df.loc[row['dna'], 'flapjackid'])
            fj_obj = self.fj.create(
                'vector',
                name=row['name'],
                description=row['description'],
                dnas=[self.df.loc[row['dna'], 'flapjackid']],
                confirm=self.confirm,
                overwrite=self.overwrite,
            )
            for i in fj_obj:
                print(i, fj_obj[i][0])
            print()
            self.hash_map[index] = fj_obj.id[0]
            if fj_obj.id[0] not in del_inds:
                del_inds.append(fj_obj.id[0])
            # if index in sbol_hash_map patch the sbol uri
            if index in self.sbol_hash_map:
                self.fj.patch('vector', fj_obj.id[0], sbol=self.sbol_hash_map[index])
            self.df.loc[index, 'flapjackid'] = fj_obj.id[0]
        self.del_map['vector'] = del_inds


    def upload_assays(self):
        del_inds = []
        for index, row in self.df[self.df['object'] == 'Assay'].iterrows():
            fj_obj = self.fj.create(
                'assay',
                study=self.df.loc[row['study'], 'flapjackid'],
                name=row['name'],
                description=row['description'],
                machine=row['machine'],
                temperature=row['temperature'],
                confirm=self.confirm,
                overwrite=self.overwrite,
            )
            for i in fj_obj:
                print(i, fj_obj[i][0])
            print()
            self.hash_map[index] = fj_obj.id[0]
            if fj_obj.id[0] not in del_inds:
                del_inds.append(fj_obj.id[0])
            # if index in sbol_hash_map patch the sbol uri
            if index in self.sbol_hash_map:
                self.fj.patch('assay', fj_obj.id[0], sbol=self.sbol_hash_map[index])
            self.df.loc[index, 'flapjackid'] = fj_obj.id[0]
        self.del_map['assay'] = del_inds


    def upload_samples(self):
        del_inds = []
        # get fj ids from sample design
        for index, row in self.df[self.df['object'] == 'Sample'].iterrows():
            media_index = self.df.loc[row['sampledesign'], 'media']
            media_id = self.df.loc[media_index, 'flapjackid']
            strain_index = self.df.loc[row['sampledesign'], 'strain']
            strain_id = self.df.loc[strain_index, 'flapjackid']
            vector_index = self.df.loc[row['sampledesign'], 'vector']
            vector_id = self.df.loc[vector_index, 'flapjackid']

            fj_obj = self.fj.create(
                'sample',
                assay=self.df.loc[row['assay'], 'flapjackid'],
                media=media_id,
                strain=strain_id,
                vector=vector_id,
                row=row['row'],
                col=row['col'],
                confirm=self.confirm,
                overwrite=self.overwrite,
            )
            for i in fj_obj:
                print(i, fj_obj[i][0])
            print()
            self.hash_map[index] = fj_obj.id[0]
            if fj_obj.id[0] not in del_inds:
                del_inds.append(fj_obj.id[0])
            # if index in sbol_hash_map patch the sbol uri
            if index in self.sbol_hash_map:
                self.fj.patch('sample', fj_obj.id[0], sbol=self.sbol_hash_map[index])
            self.df.loc[index, 'flapjackid'] = fj_obj.id[0]

            if not pd.isna(row['supplement']):
                supplement_index = self.df.loc[row['sampledesign'], 'supplement']
                supplement_id = self.df.loc[supplement_index, 'flapjackid']
                self.fj.patch('sample', fj_obj.id[0], supplements=supplement_id)
        self.del_map['sample'] = del_inds

    def upload_measurements(self):
        del_inds = []
        for index, row in self.df[self.df['object'] == 'Measurement'].iterrows():
            # print(self.df.loc[row['dna'], 'flapjackid'])
            fj_obj = self.fj.create(
                'measurement',
                sample=[self.df.loc[row['sample'], 'flapjackid']], 
                signal=[self.df.loc[row['signal'], 'flapjackid']],
                value=row['value'],
                time=row['time'],
                confirm=self.confirm,
                overwrite=self.overwrite,
            )
            for i in fj_obj:
                print(i, fj_obj[i][0])
            print()
            self.hash_map[index] = fj_obj.id[0]
            if fj_obj.id[0] not in del_inds:
                del_inds.append(fj_obj.id[0])
            self.df.loc[index, 'flapjackid'] = fj_obj.id[0]
        self.del_map['measurement'] = del_inds



    def upload_all(self):
        self.create_df()
        self.upload_studies()
        self.upload_signals()
        self.upload_chemicals()
        self.upload_dna()
        self.upload_medias()
        self.upload_strains()
        self.upload_supplements()
        self.upload_vectors()
        self.upload_assays()
        self.upload_samples()
        self.upload_measurements()

    def delete_all(self):
        for model in self.del_map:
            for id in self.del_map[model]:
                self.fj.delete(model, id, confirm=False)

    def upload_objects_in_sheets(self):
        """
        Uploads all objects in the sheets defined in self.sheet_object_hash_map
        """
        for sheet in self.sheet_object_hash_map:
            if self.sheet_object_hash_map[sheet] == 'Study':
                self.upload_studies()
            if self.sheet_object_hash_map[sheet] == 'Signal':
                self.upload_signals()
            if self.sheet_object_hash_map[sheet] == 'Chemical':
                self.upload_chemicals()
            if self.sheet_object_hash_map[sheet] == 'DNA':
                self.upload_dna()
            if self.sheet_object_hash_map[sheet] == 'Media':
                self.upload_medias()
            if self.sheet_object_hash_map[sheet] == 'Strain':
                self.upload_strains()
            if self.sheet_object_hash_map[sheet] == 'Supplement':
                self.upload_supplements()
            if self.sheet_object_hash_map[sheet] == 'Vector':
                self.upload_vectors()
            if self.sheet_object_hash_map[sheet] == 'Assay':
                self.upload_assays()
            if self.sheet_object_hash_map[sheet] == 'Sample':
                self.upload_samples()
            if self.sheet_object_hash_map[sheet] == 'Measurement':
                self.upload_measurements()
            else:
                print(f"Sheet {sheet} does not correspond to a valid flapjack object")
        # self.df.to_csv('output.csv')








