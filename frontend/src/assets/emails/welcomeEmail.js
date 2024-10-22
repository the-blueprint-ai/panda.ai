const welcome_email = `
<html>
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome Email</title>
  </head>
  <body style="display: flex; flex-direction: column; align-items: center; justify-content: flex-start; background-color: #EFEFEF; font-family: Monaco; font-size: 12px; line-height: 1.5; color: #FFFFFF; min-height: 100%; max-width: 600px; border-radius: 10px; margin: 0 auto;">   
      <table width="90%" cellpadding="0" cellspacing="0" role="presentation" style="margin-top: 20px; background-color: #000000; border-radius: 10px; text-align: center;">
          <tr>
            <td style="padding: 40px; font-size: 12px;">
              <a href="https://www.mypanda.ai?utm_source=panda.ai&utm_medium=email&utm_campaign=welcome&utm_content=logo"><img src="https://s3.eu-west-2.amazonaws.com/panda.ai/panda-standard.png" class="biglogo" width="100" /></a>
              <a href="https://www.mypanda.ai?utm_source=panda.ai&utm_medium=email&utm_campaign=welcome&utm_content=title" style="text-decoration: none;"><h1 style="font-size: 24px; font-weight: bold; text-align: center; color: #FFFFFF; margin-bottom: 20px;">WELCOME TO PANDA.AI!</h1></a>
              <p style="text-align: left;">Hi!</p>
              <p style="text-align: left;">We're thrilled to have you on board! Thank you for for taking 🐼 panda.ai out for a spin. We believe in the power of personalised AI experiences and giving users complete control over their own data.</p>
              <p style="text-align: left;">Here are some helpful links to get you started:</p>
              <ul style="list-style-type: none; padding-left: 10px;">
                <li style="padding-bottom: 5px; text-align: left;"><a href="https://www.mypanda.ai/about?utm_source=panda.ai&utm_medium=email&utm_campaign=welcome&utm_content=about" style="color: #FFCB4C; text-decoration: none;">ABOUT</a></li>
                <li style="padding-bottom: 5px; text-align: left;"><a href="https://www.mypanda.ai/roadmap?utm_source=panda.ai&utm_medium=email&utm_campaign=welcome&utm_content=roadmap" style="color: #FFCB4C; text-decoration: none;">ROADMAP</a></li>
                <li style="padding-bottom: 5px; text-align: left;"><a href="https://www.mypanda.ai/privacy?utm_source=panda.ai&utm_medium=email&utm_campaign=welcome&utm_content=privacy" style="color: #FFCB4C; text-decoration: none;">PRIVACY</a></li>
                <li style="padding-bottom: 5px; text-align: left;"><a href="https://www.mypanda.ai/support?utm_source=panda.ai&utm_medium=email&utm_campaign=welcome&utm_content=support" style="color: #FFCB4C; text-decoration: none;">SUPPORT</a></li>
              </ul>
              <p style="text-align: left;">If you have any questions, don't hesitate to reach out to our support team. We're here to help!</p>
              <p style="text-align: left;">Love & hugs,</p>
              <p style="text-align: left;"><strong>🐼</strong></p>
            </td>
          </tr>
      </table>
    <div data-role="module-unsubscribe" class="module" role="module" data-type="unsubscribe" style="color:#444444; font-size:12px; line-height:20px; padding:16px 16px 16px 16px; text-align:Center;" data-muid="4e838cf3-9892-4a6d-94d6-170e474d21e5">
      
      <p style="font-size:12px; line-height:20px; color: #000000;">
        <a href="[unsubscribe]" target="_blank" class="Unsubscribe--unsubscribeLink" style="font-family: Monaco; color: #000000; text-decoration:none;">
          UNSUBSCRIBE
        </a>
      </p>
    </div>
  </body>
</html>
`;

export default welcome_email;
