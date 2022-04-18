import SteamApps from "../SteamApps";
import SteamAppInfo from "../SteamAppInfo";
import {useEffect, useState} from "react";
import {Box, Center, Flex, Grid, GridItem, SimpleGrid, Square, Text} from "@chakra-ui/react";


const HomePage = (props) => {

    const [app, setApp] = useState(220)

    return(
        <Grid
          h='200px'
          templateRows='repeat(2, 1fr)'
          templateColumns='repeat(8, 1fr)'
          gap={4}
        >
            <GridItem rowSpan={1} colSpan={5}>
                <SteamApps setApp={setApp}/>
            </GridItem>
            <GridItem colSpan={3} rowSpan={1}>
                <SteamAppInfo appid={app}/>
            </GridItem>

        </Grid>

    )

}

export default HomePage;