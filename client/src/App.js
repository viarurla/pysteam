import logo from './logo.svg';
import './App.css';
import {QueryClient, QueryClientProvider} from "react-query";
import SteamApp from "./components/SteamApp";
import SteamApps from "./components/SteamApps";
import ClientNavBar from "./components/ClientNavBar";
import HomePage from "./components/pages/HomePage";

import {Box, ChakraProvider, Spacer, StylesProvider} from "@chakra-ui/react";
// 1. Import the extendTheme function
import { extendTheme} from '@chakra-ui/react'

// 2. Extend the theme to include custom colors, fonts, etc
const colors = {
  brand: {
    900: '#1a365d',
    800: '#153e75',
    700: '#2a69ac',
  },
}

const theme = extendTheme({ colors })
const queryClient = new QueryClient();

function App() {
    return (
        <ChakraProvider theme={theme}>
            <div className="App">
                <Box margin={10}>
                    <ClientNavBar/>
                </Box>
                <QueryClientProvider client={queryClient}>
                    <Box margin={10}><HomePage /></Box>
                </QueryClientProvider>
            </div>
        </ChakraProvider>
    );
}

export default App;

//          {/*<SteamAppGrid/>*/}
//           {/*  <HookQuery/>*/}
//           {/*  <HookMutation url={"http://127.0.0.1:8000/apps"}/>*/}