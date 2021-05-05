import React from 'react'
import { useDispatch, useSelector} from 'react-redux'
import { saveMessage } from '../_actions/message_actions'
import { List, Icon, Avatar } from 'antd'
const axios = require('axios').default

function Chatbot() {
    const dispatch = useDispatch()
    const messageFromRedux = useSelector(state => state.message.messages)

    const textQuery = async(text) => {
        
        // Show the text that user sent to server
        const conversations = []

        let conversation = {
            who: 'user',
            content: {
                text: text
            }
        }

        dispatch(saveMessage(conversation))

        conversations.push(conversation)

        // send to server

        const textQueryVariables = {
            text
        }

        try {
            const response = await axios.post('http://127.0.0.1:5000/test', textQueryVariables)
            const content = response.data // fix later
            conversation = {
                who: 'bot',
                content: content
            }
            dispatch(saveMessage(conversation))
            console.log(conversation)
            conversations.push(conversation)
            
        } catch (error) {
            conversation = {
                who: 'bot',
                content: {
                    text: "Error Error"
                }
            }
            dispatch(saveMessage(conversation))
            conversations.push(conversation)
        }
    
    }

    const keyPressHandler = (e) => {
        if(e.key === "Enter") {
            if(!e.target.value) {
                return alert("you need to type something")
            }

            textQuery(e.target.value)

            e.target.value = ""
        }

    }

    const renderOneMessage = (message, i) => {
        console.log("message",message)

        return <List.Item key={i} style={{ padding: '1rem'}}>
            <List.Item.Meta
                avatar = {<Avatar/>}
                title={message.who}
                description={message.content.text}
            
            />
        </List.Item>
    }

    const renderMessage = (returnMessages) => {

        if(returnMessages) {
            return returnMessages.map((message, i) => {
                return renderOneMessage(message, i)
            })
        }
        else {
            return null
        }

    }

    return (
        <div style={{
            height: 700, width: 700,
            border: '3px solid black', borderRadius: '7px'
        }}>

            <div style = {{ height: 644, width: '100%', overflow: 'auto'}}>
                { renderMessage(messageFromRedux) }
            </div>

            <input
                style={{
                    margin: 0, width: '100%', height: 50,
                    borderRadius: '4px', padding: '5px', fontSize: '1rem'
                }}
                placeholder="Send a message..."
                onKeyPress = {keyPressHandler}
                type="text"
            />
        
        </div>
    )
}

export default Chatbot
