import axios from "axios";
import {useQuery} from "react-query";
import {Tile} from "@carbon/react/lib/components/Tile/Tile";
import {useEffect} from "react";
import {Heading} from "@carbon/react";
import {Text} from "@chakra-ui/react";


const SteamAppInfo = (props) => {
    const fetchSteamAppInfo = async () => {
        const {data} = await axios.get(
            `http://localhost:8004/app-info/${props.appid}`
        );
        console.log(data)
        return data
    };

    const {
        isLoading,
        isSuccess,
        error,
        isError,
        data: steamAppInfoData,
        refetch
    } = useQuery("info", fetchSteamAppInfo, {enabled: false})


    useEffect(() => {
        refetch()
    }, [props.appid])

    return (
        <div>
            {isLoading && <article>...Loading user </article>}
            {isError && <article>{error.message}</article>}
            {isSuccess && (
                <Tile>
                    <Heading>{steamAppInfoData.name}</Heading>
                    <img src={steamAppInfoData.header_image} alt={""}/>
                    <Text>{steamAppInfoData.about_the_game}</Text>
                </Tile>
            )}
        </div>
    );
}

export default SteamAppInfo;