import * as React from 'react';
import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';
import { purple } from '@mui/material/colors';
import { Switch } from '@mui/material';

const StyledSwitch = styled(Switch)(({ theme }) => ({
    color: theme.palette.getContrastText(purple[500]),
    color: '#c4a35a',
    backgroundColor:  '#c4a35a',
    '&:hover': {
      backgroundColor:  '#c4a35a',
    },
  }));

export default StyledSwitch;