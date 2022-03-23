import { useRouter } from "next/router";
import { useEffect } from 'react'
import { waitForArm, moveArduino, sleep } from "../../service/backend"

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

export default function Place() {
  const router = useRouter();

  let moving = false;

  const checkArmAndMove = async () => {
    waitForArm().then(async () => {
      await moveArduino();
      moving = true;
      await sleep(30000);
      router.push("/returnfin");
    });
  };

  useEffect(checkArmAndMove, []);

  return (
    <SimpleGrid height="100vh">
      <VStack height="100%" marginTop="20%">
        {
          !moving && (
            <div>
          <Center>
            <Heading>
              Place the item on the kiosk with the label facing up
            </Heading>
          </Center>
          <Box alignContent="left">
            <a href="/">
              <button className={styles.grayButton}>
                <Text> Cancel Return </Text>
              </button>
            </a>
          </Box>
          </div>
          )
        }
        { 
          moving && (
            <div>
              <Center> 
                <Heading>
                  Returning item, please wait...
                </Heading>
              </Center> 
            </div>
          )
        }

      </VStack>
    </SimpleGrid>
  );
}
