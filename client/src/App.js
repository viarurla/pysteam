import logo from './logo.svg';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import {QueryClient, QueryClientProvider} from "react-query";
import SteamApp from "./components/SteamApp";
import SteamApps from "./components/SteamApps";

const queryClient = new QueryClient();

function App() {
  return (
    <div className="App">
      {/*<SteamAppGrid/>*/}
      {/*  <HookQuery/>*/}
      {/*  <HookMutation url={"http://127.0.0.1:8000/apps"}/>*/}
      <QueryClientProvider client={queryClient}>
        {/*<SteamApp appid={"220"}/>*/}
        <SteamApps/>
      </QueryClientProvider>
    </div>
  );
}

export default App;
