/**
 * Created by MingJe on 2015/5/16.
 */

import javax.mail.*;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;
import java.util.Properties;

public class MailSender {
    public static void main(String[] args) throws MessagingException {

        String host = "smtp.gmail.com";
        String username = "g29298@gmail.com";
        String password = "fec572nst";
        String to = "g25259@live.com";
        Properties props = new Properties();
        props.setProperty("mail.debug", "true");
        props.setProperty("mail.smtp.auth", "true");
        props.setProperty("mail.smtp.host", host);
        props.setProperty("mail.transport.protocol", "smtp");
        props.setProperty("mail.smtp.port", "587");
        props.setProperty("mail.smtp.starttls.enable", "true");

        Session session = Session.getInstance(props, new Authenticator() {
            @Override
            protected PasswordAuthentication getPasswordAuthentication() {
                return new PasswordAuthentication(username, password);
            }
        });

        Message msg = new MimeMessage(session);

        msg.setSubject("JavaMail");
        msg.setText("test");
        msg.setFrom(new InternetAddress(username));
        msg.setRecipient(Message.RecipientType.TO, new InternetAddress(to));

        Transport.send(msg);

    }
}
