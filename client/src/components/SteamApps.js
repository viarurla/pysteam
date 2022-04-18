import {useEffect, useState} from "react";
import axios from "axios";
import {useQuery} from "react-query";
import {Table, TableCaption, TableContainer, Tbody, Td, Tfoot, Th, Thead, Tr} from "@chakra-ui/react";


const SteamApps = (props) => {
    const fetchSteamApps = async () => {
        const {data} = await axios.get(
            `http://localhost:8004/apps`
        );
        return data
    };
    const {
        isLoading,
        isSuccess,
        error,
        isError,
        data: steamData
    } = useQuery("apps", fetchSteamApps);

  return (
    <div>
      {isLoading && <article>...Loading user </article>}
      {isError && <article>{error.message}</article>}
      {isSuccess && (
        <TableContainer>
          <Table variant='simple'>
            <TableCaption>Imperial to metric conversion factors</TableCaption>
            <Thead>
              <Tr>
                <Th>appid</Th>
                <Th>name</Th>
              </Tr>
            </Thead>
            <Tbody>
                {steamData.map((sd) =>
                    <Tr key={sd.appid} onClick={() => props.setApp(sd.appid)}>
                        <Td>{sd.appid}</Td>
                        <Td>{sd.name}</Td>
                    </Tr>
                )}
            </Tbody>
            <Tfoot>
              <Tr>
                <Th>To convert</Th>
                <Th>into</Th>
                <Th isNumeric>multiply by</Th>
              </Tr>
            </Tfoot>
          </Table>
        </TableContainer>
        // <Table striped bordered hover size="sm">
        //   <thead>
        //     <tr>
        //       <th>appid</th>
        //       <th>name</th>
        //     </tr>
        //   </thead>
        //   <tbody>
        //   {steamData.map((sd) =>
        //       <tr onSelect={() => props.onClick(sd.appid)}>
        //       <td>{sd.appid}</td>
        //       <td>{sd.name}</td>
        //     </tr>
        //   )}
        //
        //   </tbody>
        // </Table>
      )}
    </div>
  );
}

export default SteamApps;