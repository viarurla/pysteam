import {useQuery} from "react-query";
import axios from "axios";


const SteamApp = (props) => {
    const fetchSteamApp = async () => {
        const {data} = await axios.get(
            `http://localhost:8000/apps/${props.appid}`
        );
        return data
    };
    const {
        isLoading,
        isSuccess,
        error,
        isError,
        data: steamData
    } = useQuery("appid", fetchSteamApp);

  return (
    <div>
      {isLoading && <article>...Loading user </article>}
      {isError && <article>{error.message}</article>}
      {isSuccess && (
        <article>
          <p>Steam App: {steamData.name}</p>
        </article>
      )}
    </div>
  );
};
export default SteamApp;