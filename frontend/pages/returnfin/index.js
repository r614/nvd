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

export default function Wait() {
  const router = useRouter();

  return (
    <SimpleGrid height="100vh">
      <VStack height="100%" marginTop="20%">
        <Center>
          <Heading>
          Item submitted successfully!
        </Heading>
        </Center>
        <HStack spacing="2">
            <a href="/success"> 
                <Button size="lg" bg="#3AC572" color="white"> 
                    Start another return 
                </Button>
            </a>
            <a href="/success"> 
                <Button size="lg" bg="#D7D9D8"> 
                    Return another item
                </Button>
            </a>
        </HStack>
      </VStack>
    </SimpleGrid>
  );
}
