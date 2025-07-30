

from scipy import stats

class Bernoulli:
    def __init__(self, p):
        """
        Inizializza il generatore con una distribuzione di Bernoulli con parametro p.
        
        Args:
            p (float): Un valore tra 0 e 1 che rappresenta la probabilità di estrarre 1.
                       Se p = 0, estrai() restituirà sempre 0.
                       Se p = 1, estrai() restituirà sempre 1.
        """
        if not 0 <= p <= 1:
            raise ValueError("La probabilità p deve essere compresa tra 0 e 1")
        self.p = p
        self.bernoulli = stats.bernoulli(p)
    
    def estrai(self):
        """
        Estrae un valore secondo la distribuzione di Bernoulli con parametro p.
        
        Returns:
            int: 1 con probabilità p, 0 con probabilità (1-p).
        """
        return self.bernoulli.rvs(1)[0]

prof_italiano = Bernoulli(1/2)
prof_informatica = Bernoulli(1/3)
