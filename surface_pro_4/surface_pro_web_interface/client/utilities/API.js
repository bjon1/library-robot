

const request = async (method, url, body=null, headers=null) => {

    if(!headers) {
        headers = {
            'Content-Type': 'application/json'
        }
    }

    const options = body ? { method, headers, body: JSON.stringify(body) } : { method, headers }
    let response

    try {
        response = await fetch(url, options)
    } catch (error) {
        console.error('Error:', error.message)
        console.error("Details:", error.details)
    }

    if(response.ok) {
        return response.json()
    } else {
        console.error('Error:', response.status)
        console.error('Details:', response.statusText)
    }

}

export { request }