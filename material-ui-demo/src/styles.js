import { makeStyles } from '@material-ui/core/styles';

// Vytvoření stylů
const useStyles = makeStyles((theme) => ({
  container: {
    backgroundColor: theme.palette.background.paper,
    padding: theme.spacing(8, 0, 6)
  },
  icon: {
    marginRight: '20px',
  },
  buttons: {
    marginTop: '40px'
  },
  cardGrid: {
    padding: '20px 0'
  },
  card: {
    height: 'auto',
    display: 'flex',
    flexDirection: 'column'
  },
  cardMedia: {
    paddingTop: '56.25%' // Udržuj to pro aspect ratio (16:9)
  },
  cardContent: {
    flexGrow: 1,
  },
  footer: {
    backgroundColor: theme.palette.background.paper,
    padding: '50px 0'
  }
}));

export default useStyles;
