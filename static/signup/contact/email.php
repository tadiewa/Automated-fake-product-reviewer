<?php

$name = $_POST['name'];
$email = $_POST['email'];
$subject = "InTheme";
$message = $_POST['message'];

require 'PHPMailer/PHPMailerAutoload.php';

$mail = new PHPMailer;

//$mail->SMTPDebug = 3;                               // Enable verbose debug output

$mail->isSMTP();                                      // Set mailer to use SMTP
$mail->Host = 'mail.99webpage.com ';  // Specify main and backup SMTP servers
$mail->SMTPAuth = true;                               // Enable SMTP authentication
$mail->Username = 'nce18cex@99webpage.com';                 // SMTP username
$mail->Password = 'restubumi2606';                           // SMTP password
$mail->SMTPSecure = 'tls';                            // Enable TLS encryption, `ssl` also accepted
$mail->Port = 587;                                    // TCP port to connect to

$mail->setFrom($email, $name);
$mail->addAddress('nce18cex@gmail.com', 'InTheme');     // Add a recipient

$mail->isHTML(true);                                  // Set email format to HTML

$mail->Subject = $subject;
$mail->Body    = $message;

if(!$mail->send()) {
    echo "
        <div id='failed' class='alert alert-danger'>
            <button type='button' class='close' data-dismiss='alert'>&times;</button>
            Sorry your message <strong>failed</strong> to send. check the connection!<br />
        </div>	
    ";
    echo "
		<div class='alert alert-info'>
			<button type='button' class='close' data-dismiss='alert'>&times;</button> " . $mail->ErrorInfo . "<br />
		</div>
	";
} else {
    echo "
        <div class='alert alert-success' role='alert' data-out='bounceOut'>
            <button type='button' class='close' data-dismiss='alert'>&times;</button>
            <i class='fa fa-check'></i> 
            <h6 class='title'>Success</h6>
            <strong>Congratulation</strong> Your message has been sent. Thank you!<br />
        </div>
    ";
}