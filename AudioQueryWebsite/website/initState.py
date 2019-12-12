from .StateClass import stateClass
import pickle

if __name__ =="__main__":
    s = stateClass()
    stateClass.__module__ = "StateClass"
    pickle.dump(s, open('state.p', 'rb'))
    
    
