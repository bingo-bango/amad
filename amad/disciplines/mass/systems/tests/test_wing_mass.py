import pytest
from amad.disciplines.mass.systems import WingMass
from amad.disciplines.mass.systems import AbstractMassComponent


@pytest.fixture
def factory():
    def factory_impl(model, tech_bracing, m_mto, m_mzf):
        syst = WingMass(name="wingweight", model=model)

        parameters = {
            "m_mto": m_mto,
            "m_mzf": m_mzf,
            "tech_bracing": tech_bracing,
            "r_wing_taper": 0.3,
            "chord_wing_root": 1.1763661651646,
            "n_ult": 3.3,
            "x_wing_span": 18.511,
            "t_wing_root_chord": 0.091755,
            "delta_wing_sweep": 15.0,
            "r_wing_aspect": 12.1049,
            "v_fuel_fuse": 0.0619038,
        }

        for p in parameters:
            try:
                syst[p] = parameters[p]
            except KeyError:
                continue

        return syst

    return factory_impl


@pytest.mark.parametrize(
    "model, expected_wing_mass, tech_bracing, m_mto, m_mzf",
    [
        ("simpleac", 154.64, "none", 887.3414, 581.5310),
        ("cessna", 301.13, "none", 887.3414, 581.5310),
        ("cessna", 219.33, "strut", 887.3414, 581.5310),
        ("torenbeek", 145.16, "none", 887.3414, 581.5310),
        ("torenbeek", 529.13, "none", 5896.761, 3628.776),
        ("specified", 123.0, "none", 1.0, 1.0),
    ],
)
def test_WingMass_run_once(
    factory, model, expected_wing_mass, tech_bracing, m_mto, m_mzf
):
    wing = factory(model, tech_bracing, m_mto, m_mzf)
    wing.run_once()
    result = wing.total.mass
    assert result == pytest.approx(expected_wing_mass, rel=1e-4)


def test_WingMass_models():
    """Test available model dictionary"""
    models = WingMass.models()
    assert list(models) == ["simpleac", "cessna", "torenbeek", "specified"]
    for stype in models.values():
        assert issubclass(stype, AbstractMassComponent)
