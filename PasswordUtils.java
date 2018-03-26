import java.security.GeneralSecurityException;
import java.security.MessageDigest;
import java.security.SecureRandom;

import org.apache.commons.codec.DecoderException;
import org.apache.commons.codec.binary.Hex;
import org.apache.commons.lang3.StringUtils;
import org.apache.commons.lang3.Validate;

/**
 * ���빤����
 * ����commons-lang3��commons-codec
 * @className PasswordUtils.java
 * @author jitwxs
 * @version ����ʱ�䣺2017��10��18�� ����9:18:38
 */
public class PasswordUtils {
	public static final int HASH_INTERATIONS = 1024;
	public static final int SALT_SIZE = 8;
	private static final String SHA1 = "SHA-1";
	
	private static SecureRandom random = new SecureRandom();

	/**
	 * ���ɰ�ȫ�����룬���������16λsalt������1024�� sha-1 hash
	 * @author jitwxs
	 * @version ����ʱ�䣺2017��10��18�� ����9:10:31 
	 * @param plainPassword ����
	 * @return ����(56λ)
	 */
	public static String entryptPassword(String plainPassword) {
		byte[] salt = generateSalt(SALT_SIZE);
		byte[] hashPassword = sha1(plainPassword.getBytes(), salt, HASH_INTERATIONS);
		return encodeHex(salt)+encodeHex(hashPassword);
	}
	
	/**
	 * ��֤����
	 * @author jitwxs
	 * @version ����ʱ�䣺2017��10��18�� ����9:11:18 
	 * @param plainPassword ����
	 * @param password ����
	 * @return ��֤���
	 */
	public static boolean validatePassword(String plainPassword, String password) {
		byte[] salt = decodeHex(password.substring(0,16));
		byte[] hashPassword = sha1(plainPassword.getBytes(), salt, HASH_INTERATIONS);
		return password.equals(encodeHex(salt)+encodeHex(hashPassword));
	}

	/**
	 * �������ǿ��
	 * @author jitwxs
	 * @version ����ʱ�䣺2018��3��8�� ����10:50:06 
	 * @param password
	 * @return ��|��|ǿ|δ֪
	 */
	public static String checkStrength(String password) {
        String regexZ = "\\d*", regexS = "[a-zA-Z]+", regexT = "\\W+$";
        String regexZT = "\\D*", regexST = "[\\d\\W]*", regexZS = "\\w*";
        String regexZST = "[\\w\\W]*";
  
        if(!StringUtils.isEmpty(password)) {
        	if (password.matches(regexZ) || password.matches(regexS) || password.matches(regexT)) {
                return "��";
            } else if (password.matches(regexZT) || password.matches(regexST) || password.matches(regexZS)) {
                return "��";
            } else if (password.matches(regexZST)) {
                return "ǿ";
            }
        }
        return "δ֪";
    } 

	private static byte[] generateSalt(int numBytes) {
		Validate.isTrue(numBytes > 0, "numBytes argument must be a positive integer (1 or larger)", numBytes);
		byte[] bytes = new byte[numBytes];
		random.nextBytes(bytes);
		return bytes;
	}

	private static String encodeHex(byte[] input) {
		return new String(Hex.encodeHex(input));
	}

	private static byte[] decodeHex(String input) {
		try {
			return Hex.decodeHex(input.toCharArray());
		} catch (DecoderException e) {
			return null;
		}
	}

	private static byte[] sha1(byte[] input, byte[] salt, int iterations) {
		return digest(input, SHA1, salt, iterations);
	}

	private static byte[] digest(byte[] input, String algorithm, byte[] salt, int iterations) {
		try {
			MessageDigest digest = MessageDigest.getInstance(algorithm);
			if (salt != null) {
				digest.update(salt);
			}
			byte[] result = digest.digest(input);

			for (int i = 1; i < iterations; i++) {
				digest.reset();
				result = digest.digest(result);
			}
			return result;
		} catch (GeneralSecurityException e) {
			return null;
		}
	}

	public static void main(String[] args) {
		String entryptPassword = entryptPassword("123");
		System.out.println(entryptPassword);
		boolean flag = validatePassword("123", entryptPassword);
		System.out.println(flag);
		System.out.println(checkStrength("123"));
	}
}