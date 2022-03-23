import { useRouter } from "next/router";
import styles from "../../styles/Home.module.css";
import {
  SimpleGrid,
  Box,
  Center,
  Heading,
  Text,
  Button,
  VStack,
  HStack
} from "@chakra-ui/react";

const dataTable = {
  1234: {
    store: "Lululemon",
    items: [
      {
        itemName: "City Sweat Joggers in Black (M)",
        price: "$80.57",
      },
      {
        itemName: "City Sweat Hoodie in Gray (M)",
        price: "$100.57",
      },
      {
        itemName: "Wowowow Jeans (M)",
        price: "$420.69",
      },
    ],
  },
};

export default function Return() {
  const router = useRouter();
  const { id } = router.query;

  return (
    <SimpleGrid columns={2}>
      <Box width="50vh" height="100vh" justifyContent="left">
        <Center marginTop="65%" marginLeft="25%" overflow={false} width="50vh">
          <Heading size="4xl">Choose the item being returned</Heading>
        </Center>

        <Box marginLeft="25%">
          <footer className={styles.footer}>
            <a href="/">
              <button className={styles.grayButton}>
                <Text> Cancel Return </Text>
              </button>
            </a>
          </footer>
        </Box>
      </Box>
      <Box bg="#E4E4E4" width="100%" height="100vh">
        <Box marginLeft="3.5%" marginTop="149px">
          <Heading fontSize="70px">Order #{id}</Heading>
        </Box>
        <Box marginLeft="3.5%">
          {id in dataTable && (
            <Text fontSize="35px" fontWeight="thin">
              Store: {dataTable[id]["store"]}
            </Text>
          )}
        </Box>
        <Center width="100%" marginTop="2%">
          <VStack>
            {id in dataTable &&
              Object.keys(dataTable[id]["items"]).map((x) => (
                <Box>
                  <Button
                    bg="#C4C4C4"
                    size="lg"
                    width="700px"
                    height="100px"
                    onClick={() => router.push("/place")}
                  >
                    <HStack justifyContent="space-between" width="100%">
                        <Text fontSize="25px" fontWeight="light" textAlign="left">
                          {dataTable[id]["items"][x]["itemName"]}
                        </Text>
                        <Text fontSize="25px" fontWeight="strong" textAlign="right">
                          {dataTable[id]["items"][x]["price"]}
                        </Text>
                    </HStack>
                  </Button>
                </Box>
              ))}
          </VStack>
        </Center>
      </Box>
    </SimpleGrid>
  );
}
