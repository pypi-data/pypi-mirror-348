// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/TauFinder.hh"
#include "Rivet/Tools/Utils.hh"

namespace Rivet {


  /// @brief High-mass Drell-Yan prototype at 13 TeV
  class ATLAS_STDM_2021_10 : public Analysis {
  public:

    /// Constructor
    RIVET_DEFAULT_ANALYSIS_CTOR(ATLAS_STDM_2021_10);
    //@}


    /// @name Analysis methods
    //@{

    /// Book histograms and initialise projections before the run
    void init() {

      // Basic final-state projection
      const FinalState fs(Cuts::abseta < 4.9);

      const TauFinder hadtaus(TauDecay::HADRONIC);
      declare(hadtaus, "hadtaus");

      const vector<double> b_mll = {100.0, 145.0, 160.0, 175.0, 205.0, 235.0, 275.0, 315.0, 355.0, 395.0, 455.0, 515.0, 635.0};
      book(_h, "_mll",    b_mll);
      book(_e, "mll", b_mll);

    }

    /// Perform the per-event analysis
    void analyze(const Event& event) {

      // visible.
      const vector<Particle> hadtaus = apply<TauFinder>(event, "hadtaus").taus();

      std::vector<double> pTlep;
      double mll;

      FourMomentum p;
      for (const Particle& tau : hadtaus) {
        FourMomentum l;
        for (const Particle& part : tau.children()) {
          if (part.isNeutrino())  continue;
          p += part.mom();
          l += part.mom();
        }
        if ((l.abseta() > 1.37) && (l.abseta() < 1.52 || l.abseta() > 2.47))  continue;
        if (l.pT() < 20*GeV) continue;
        pTlep.push_back(l.pT());
      }

      if (pTlep.size() != 2) vetoEvent;
      mll = p.mass();

      std::sort(pTlep.begin(), pTlep.end(), std::greater<double>());
      if (pTlep[0] < 90*GeV) vetoEvent;
      if (pTlep[1] < 60*GeV) vetoEvent;
      if (mll <= 100*GeV)  vetoEvent;

      //histogram filling
      _h->fill(mll/GeV);

    }

    /// Normalise histograms etc., after the run
    void finalize() {

      scale(_h, crossSectionPerEvent()/femtobarn);
      * _e = _h->mkEstimate(_e->path(), "stats");
      size_t idx = _e->numBins()+1;
      _e->bin(idx).set(_h->bin(idx).sumW(), _h->bin(idx).errW(), "stats");

    }

    //@}

    /// @name Histograms
    //@{
    Histo1DPtr _h;
    Estimate1DPtr _e;
    //@}

  };

  RIVET_DECLARE_PLUGIN(ATLAS_STDM_2021_10);

}
