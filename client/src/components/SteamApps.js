import {useEffect, useState} from "react";
import {Table} from "react-bootstrap";
import axios from "axios";
import {useQuery} from "react-query";


const SteamApps = (props) => {
    const fetchSteamApps = async () => {
        const {data} = await axios.get(
            `http://localhost:8000/apps`
        );
        return data
    };
    const {
        isLoading,
        isSuccess,
        error,
        isError,
        data: steamData
    } = useQuery("", fetchSteamApps);

  return (
    <div>
      {isLoading && <article>...Loading user </article>}
      {isError && <article>{error.message}</article>}
      {isSuccess && (
        <Table striped bordered hover size="sm">
          <thead>
            <tr>
              <th>appid</th>
              <th>name</th>
            </tr>
          </thead>
          <tbody>
          {steamData.map((sd) =>
              <tr>
              <td>{sd.appid}</td>
              <td>{sd.name}</td>
            </tr>
          )}

          </tbody>
        </Table>
      )}
    </div>
  );
}

export default SteamApps;