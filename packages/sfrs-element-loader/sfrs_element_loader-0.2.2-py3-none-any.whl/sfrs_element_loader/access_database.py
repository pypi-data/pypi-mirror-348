import os
from dotenv import load_dotenv
from tabulate import tabulate
import inspect
import numpy as np

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .model import (
    Element, Dipole, Quadrupole, Sextupole, Octupole, Steerer, Drift,
    ExperimentalChamber, EmptyDetector, BeamStopper, ProfileGrid,
    HorizontalSlit, PlasticScintillator, RotaryWedgeDegrader,
    SlidableWedgeDegrader, LadderSystemDegrader
)

class ElementLoader:
    def __init__(self, env_path: str = '.env'):
        self._load_env(env_path)
        self._setup_database()
        
    def _load_env(self, env_path: str):
        load_dotenv(env_path)
        self.database_uri = os.getenv('SQLALCHEMY_DATABASE_URI')
        if not self.database_uri:
            raise ValueError("Database URI not found in environment variables")

    def _setup_database(self):
        engine = create_engine(self.database_uri)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def load_element_data(self, element_name: str) -> dict:
        element = self.session.query(Element).filter(Element.element_name == element_name).first()
        if not element:
            raise ValueError(f"Element '{element_name}' not found in the database")

        # Dynamically collect fields for the specific subclass of the element
        model_class = type(element)
        columns = model_class.__mapper__.column_attrs
        data = {col.key: getattr(element, col.key) for col in columns}

        # Optional: Add related objects dynamically (like experimental_chamber)
        # You can inspect relationships using `__mapper__.relationships`
        for rel in model_class.__mapper__.relationships:
            related_obj = getattr(element, rel.key)
            if related_obj:
                data[rel.key] = {
                    col.key: getattr(related_obj, col.key)
                    for col in type(related_obj).__mapper__.column_attrs
                }

        return data
    
    def list_all_optical_elements(self):
        elements = self.session.query(Element).all()
        return [element.element_name for element in elements]


    def list_all_drifts(self, pprint = False):
        """
        Retrieve all Drift elements from the database and optionally print them in a table.
        Args: pprint (bool, optional): If True, prints the drift data in a fancy grid table. Defaults to False.
        Returns: List[str]: A list of all drift element names.\n
        """
        drifts = self.session.query(Drift).all()
        drift_data = []

        for drift in drifts:
            drift_data.append({
                'element_name': drift.element_name,
                'location': drift.loc,
                'high_energy_branch': drift.high_energy_branch,
                'low_energy_branch': drift.low_energy_branch,
                'ring_branch': drift.ring_branch,
            })

        headers = ["Element Name", "High Energy Branch", "Low Energy Branch", "Ring Branch"]
        table = [
            [
                d['element_name'],
                d['high_energy_branch'],
                d['low_energy_branch'],
                d['ring_branch']
            ]
            for d in drift_data
        ]
        if pprint: print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
        return [d['element_name'] for d in drift_data]
    
    def list_all_dipoles(self, pprint = False):
        """
        Retrieve all Dipoles elements from the database and optionally print them in a table.
        Args: pprint (bool, optional): If True, prints the drift data in a fancy grid table. Defaults to False.
        Returns: List[str]: A list of all dipole element names.\n
        """
        dipoles = self.session.query(Dipole).all()
        dipole_data = []

        for dipole in dipoles:
            dipole_data.append({
                'element_name': dipole.element_name,
                'location': dipole.loc,
                'high_energy_branch': dipole.high_energy_branch,
                'low_energy_branch': dipole.low_energy_branch,
                'ring_branch': dipole.ring_branch,
            })

        headers = ["Element Name", "High Energy Branch", "Low Energy Branch", "Ring Branch"]
        table = [
            [
                d['element_name'],
                d['high_energy_branch'],
                d['low_energy_branch'],
                d['ring_branch']
            ]
            for d in dipole_data
        ]
        if pprint: print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
        return [d['element_name'] for d in dipole_data]

    def list_all_quadrupoles(self, pprint = False):
        pass

    def list_all_sextupoles(self, pprint = False):
        pass

    def list_all_octupoles(self, pprint = False):
        pass

    def list_all_multipletts(self, pprint = False):
        elements = self.session.query(Element).all()
        multiplett_names = [
            element.multiplett_company_name 
            for element in elements 
            if hasattr(element, 'multiplett_company_name') and element.multiplett_company_name is not None
        ]
        multiplett_list = np.unique(multiplett_names)

        if pprint:
            print(multiplett_list)
        return multiplett_list

    def list_magnets_in_multiplett(self, multiplett_name):
        magnets_in_multipletts = []
        positions_in_multiplett = []

        for model_class in [Quadrupole, Sextupole, Octupole, Steerer]:
            magnets = (
                self.session.query(model_class)
                .filter(model_class.multiplett_company_name == multiplett_name)
                .all()
            )
            for magnet in magnets:
                magnets_in_multipletts.append(magnet)
                positions_in_multiplett.append(magnet.position_in_multiplett)


        sorted_magnets_in_multipletts = [magnets_in_multipletts[i] for i in sorted(range(len(positions_in_multiplett)), key=lambda k: positions_in_multiplett[k])]
        return sorted_magnets_in_multipletts

    def help(self):
        print("Available methods:\n")
        for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
            if not name.startswith('_') and name != "help":
                doc = inspect.getdoc(method) or "No description"
                print(f"{name}:\n{doc}\n")


if __name__ == "__main__":                                                                                                                                                                                                                                                                                                                                                                                              
    loader = ElementLoader(env_path = '../../.env')
    element_name = 'FTF1QT21'  # adjust as needed
    data = loader.list_magnets_in_multiplett('LM20')
    print(data)
    #loader.help()

