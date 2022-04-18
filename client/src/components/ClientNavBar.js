import {Menu, MenuButton, Button, MenuItem, MenuList, Flex, Box, Spacer, Divider} from "@chakra-ui/react";
import {ChevronDownIcon} from "@chakra-ui/icons";
import {Heading} from "@carbon/react";


const ClientNavBar = (props) => {

    return (
        <Box>
            <Flex rounded={"true"}>
              <Box p='2'>
                <Heading size="md">PySteam Client</Heading>
              </Box>
              <Spacer />
              <Box>
                {/*<Button colorScheme='teal' mr='4'>*/}
                {/*  Sign Up*/}
                {/*</Button>*/}
                {/*<Button colorScheme='teal'>Log in</Button>*/}
              </Box>
            </Flex>
            <Divider/>
        </Box>
    )

}

export default ClientNavBar;