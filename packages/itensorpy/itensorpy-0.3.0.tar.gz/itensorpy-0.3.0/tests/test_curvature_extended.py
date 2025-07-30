import pytest
from sympy import symbols, Matrix, sin, cos, exp, simplify, Function
from itensorpy import Metric, ChristoffelSymbols, RiemannTensor, CurvatureInvariants
from itensorpy.spacetimes import minkowski_metric, schwarzschild_metric, kerr_metric, kerr_newman_metric
from itensorpy.spacetimes import flrw_metric, de_sitter_metric_static, anti_de_sitter_metric

class TestCurvatureExtended:
    
    def test_curvature_from_minkowski(self):
        # Test dla metryki Minkowskiego
        metric = minkowski_metric()
        curvature = CurvatureInvariants(metric)
        
        # Wszystkie niezmienniki krzywizny powinny być zerowe
        assert curvature.kretschmann() == 0
        assert curvature.chern_pontryagin() == 0
        assert curvature.euler() == 0
    
    def test_curvature_from_schwarzschild(self):
        # Test dla metryki Schwarzschilda
        r, theta, phi = symbols('r theta phi')
        metric = schwarzschild_metric(r, theta, phi)
        curvature = CurvatureInvariants(metric)
        
        # Kretschmann scalar powinien być proporcjonalny do 1/r^6
        kretschmann = curvature.kretschmann()
        assert kretschmann != 0
        
        # Test dla innych niezmienników
        assert curvature.chern_pontryagin() == 0  # Powinno być 0 dla metryki Schwarzschilda
        
        # Sprawdzenie wartości eulera
        euler = curvature.euler()
        assert euler != 0
    
    def test_kerr_metric_creation(self):
        # Test tylko utworzenia metryki Kerra bez obliczania niezmienników
        r, theta, phi, a = symbols('r theta phi a')
        metric = kerr_metric(r, theta, phi, a)
        
        # Sprawdź czy metryka ma spodziewany kształt
        assert metric.dimension == 4
        assert metric.g[0, 3] != 0  # Powinna mieć niezerowy element g_t_phi
        assert metric.g[3, 0] != 0  # Powinien być symetryczny
        
        # Sprawdź czy metryka ma oczekiwane współrzędne i parametry
        assert len(metric.coordinates) == 4
        assert r in metric.coordinates
        assert theta in metric.coordinates
        assert phi in metric.coordinates
    
    def test_kerr_newman_metric_creation(self):
        # Test tylko utworzenia metryki Kerra-Newmana bez obliczania niezmienników
        r, theta, phi, a, q = symbols('r theta phi a q')
        metric = kerr_newman_metric(r, theta, phi, a, q)
        
        # Sprawdź czy metryka ma spodziewany kształt
        assert metric.dimension == 4
        assert metric.g[0, 3] != 0  # Powinna mieć niezerowy element g_t_phi
        assert metric.g[3, 0] != 0  # Powinien być symetryczny
        
        # Sprawdź czy metryka ma oczekiwane współrzędne i parametry
        assert len(metric.coordinates) == 4
        assert r in metric.coordinates
        assert theta in metric.coordinates
        assert phi in metric.coordinates
        
        # Sprawdź czy w parametrach metryki występuje parametr ładunku q
        params_as_str = [str(p) for p in metric.params]
        assert 'q' in params_as_str or 'Q' in params_as_str
    
    def test_flrw_metric_creation(self):
        # Test tylko utworzenia metryki FLRW bez obliczania niezmienników
        t, r, theta, phi = symbols('t r theta phi')
        a_func = Function('a')
        a = a_func(t)
        metric = flrw_metric(t, r, theta, phi, a, 0)
        
        # Sprawdź czy metryka ma spodziewany kształt
        assert metric.dimension == 4
        assert metric.g[0, 0] == -1  # g_tt powinno być -1
        
        # Sprawdź czy g_rr zależy od a(t)
        assert a in metric.g[1, 1].free_symbols or t in metric.g[1, 1].free_symbols
        
        # Dla płaskiej metryki FLRW sprawdź czy jest naprawdę płaska
        flat_space = flrw_metric(t, r, theta, phi, 1, 0)
        assert flat_space.g[0, 0] == -1
        assert flat_space.g[1, 1] == 1
        assert flat_space.g[2, 2] == r**2
        assert flat_space.g[3, 3] == (r*sin(theta))**2
    
    def test_de_sitter_creation(self):
        # Test tylko utworzenia metryki de Sittera bez obliczania niezmienników
        r, theta, phi = symbols('r theta phi')
        metric = de_sitter_metric_static(r, theta, phi)
        
        # Sprawdź czy metryka ma spodziewany kształt
        assert metric.dimension == 4
        assert len(metric.coordinates) == 4
        
        # Sprawdź czy metryka jest diagonalna
        for i in range(4):
            for j in range(4):
                if i != j:
                    assert metric.g[i, j] == 0
    
    def test_anti_de_sitter_creation(self):
        # Test tylko utworzenia metryki anty-de Sittera bez obliczania niezmienników
        r, theta, phi = symbols('r theta phi')
        metric = anti_de_sitter_metric(r, theta, phi)
        
        # Sprawdź czy metryka ma spodziewany kształt
        assert metric.dimension == 4
        assert len(metric.coordinates) == 4
        
        # Sprawdź czy metryka jest diagonalna
        for i in range(4):
            for j in range(4):
                if i != j:
                    assert metric.g[i, j] == 0
    
    def test_curvature_edge_cases(self):
        # Test dla przypadków brzegowych
        
        # Tworzenie pustej metryki 2D
        x, y = symbols('x y')
        empty_metric = Metric([[0, 0], [0, 0]], [x, y])
        
        # Powinien zgłosić błąd przy próbie obliczenia niezmienników (metryka osobliwa)
        with pytest.raises(Exception):
            CurvatureInvariants(empty_metric)
        
        # Test dla niekompatybilnych wymiarów
        with pytest.raises(ValueError):
            # Próba utworzenia CurvatureInvariants dla 2D metryki 
            # (niezmienniki wymagają co najmniej 3D)
            metric_2d = Metric([[1, 0], [0, 1]], [x, y])
            CurvatureInvariants(metric_2d).kretschmann()
    
    def test_curvature_from_christoffel(self):
        # Test tworzenia niezmienników bezpośrednio z symboli Christoffela
        r, theta, phi = symbols('r theta phi')
        metric = schwarzschild_metric(r, theta, phi)
        christoffel = ChristoffelSymbols(metric)
        riemann = RiemannTensor(metric)
        
        # Utworzenie CurvatureInvariants z tensora Riemanna
        curvature = CurvatureInvariants(metric, riemann=riemann)
        
        # Sprawdzenie niezmienników
        kretschmann = curvature.kretschmann()
        assert kretschmann != 0
        
        # Porównanie z CurvatureInvariants utworzonym bezpośrednio z metryki
        direct_curvature = CurvatureInvariants(metric)
        assert simplify(kretschmann - direct_curvature.kretschmann()) == 0 