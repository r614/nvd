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
} from "@chakra-ui/react";

export default function Success() {
  const router = useRouter();

  return (
    <SimpleGrid height="100vh">
      <VStack height="100%" marginTop="20%">
        <Center>
          <Heading>
            You have finished returning all of your items! 
          </Heading>
        </Center>
        <Box alignContent="left">
          <a href="/">
            <button className={styles.grayButton}>
              <Text> Exit </Text>
            </button>
          </a>
        </Box>
      </VStack>
    </SimpleGrid>
  );
}
