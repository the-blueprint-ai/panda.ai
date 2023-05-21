const support_send_email = (confirmedEmail, message) =>
  `
<html>
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>New Support Ticket Raised</title>
  </head>
  <body style="display: flex; flex-direction: column; align-items: center; justify-content: flex-start; padding: 20px; background-color: #EFEFEF; font-family: Monaco; font-size: 12px; line-height: 1.5; color: #000000; text-decoration: none; min-height: 100%; max-width: 600px; border-radius: 10px; margin: 0 auto;">   
      <table width="90%" cellpadding="0" cellspacing="0" role="presentation" style="margin-top: 20px; color: #FFFFFF; background-color: #000000; border-radius: 10px; text-align: center;">
          <tr>
            <td style="padding: 40px; font-size: 12px;">
              <a href="https://www.mypanda.ai?utm_source=panda.ai&utm_medium=email&utm_campaign=support_request&utm_content=logo"><img src="https://s3.eu-west-2.amazonaws.com/panda.ai/panda-standard.png" class="biglogo" width="100" /></a>
              <a href="https://www.mypanda.ai?utm_source=panda.ai&utm_medium=email&utm_campaign=support_request&utm_content=title" style="text-decoration: none;"><h1 style="font-size: 24px; font-weight: bold; text-align: center; color: #FFFFFF; margin-bottom: 20px;">SUPPORT REQUEST</h1></a>
              <h2 style="text-align: left;">We've received a support request from:</h2>
              <p style="text-align: left;"><a style="color: #FFFFFF; text-decoration: none;">` +
  confirmedEmail +
  `</a></p>
              <h2 style="text-align: left;"><strong>Message as follows:</strong></h2>
              <p style="text-align: left;">` +
  message +
  `</p>
            </td>
          </tr>
      </table>
    <div data-role="module-unsubscribe" class="module" role="module" data-type="unsubscribe" style="color:#444444; font-size:12px; line-height:20px; padding:16px 16px 16px 16px; text-align:Center;" data-muid="4e838cf3-9892-4a6d-94d6-170e474d21e5">
      
      <p style="font-size:12px; line-height:20px; color: #000000;">
        <a href="[unsubscribe]" target="_blank" class="Unsubscribe--unsubscribeLink" style="font-family: Monaco; color: #000000; text-decoration:none;">
          DO NOT UNSUBSCRIBE!
        </a>
      </p>
    </div>
  </body>
</html>
`;

export default support_send_email;
