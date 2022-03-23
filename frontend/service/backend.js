const BASE_URL = "0.0.0.0:8000"

const moveArduino = async () => {
    const res = await fetch(`${BASE_URL}/move`)
    console.log(res);
}

const pingArduino = async () => { 
    const res = await fetch(`${BASE_URL}/status`)
    console.log(res);
    return res.json()["status"]
}

const sleep = (time) => {
    return new Promise((resolve) => setTimeout(resolve, time));
}

const waitForArm = async () => { 
    let status = await pingArduino()

    let retries = 0
    const retryMax = 50
    do { 
        status = await pingArduino()
        retries++
        
        if (retries == retryMax) {
            console.log("Hit 50 retries waiting for arduino for arm") 
            return
        }

        await sleep(500)

    } while (status != "armed")
}

const cancelTrigger = async () => { 
    const res = await fetch(`${BASE_URL}/cancel`) 
    console.log(res);
}