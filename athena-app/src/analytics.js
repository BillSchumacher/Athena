import ReactGA from 'react-ga4';

ReactGA.initialize([
    {
      trackingId: "G-B3SJV6NBL0",
    },
]);

export const initGA = (trackingID) => {
  ReactGA.initialize(trackingID);
};

export const logPageView = () => {
  ReactGA.set({ page: window.location.pathname });
  ReactGA.send({ hitType: "pageview", page: window.location.pathname, title: window.title });
};

export const logEvent = (category = '', action = '') => {
  if (category && action) {
    ReactGA.event({ category, action });
  }
};

export const logException = (description = '', fatal = false) => {
  if (description) {
    ReactGA.exception({ description, fatal });
  }
};
