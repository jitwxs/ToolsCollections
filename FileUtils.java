package jit.wxs.utils;

import org.apache.commons.fileupload.FileItem;
import org.apache.commons.fileupload.disk.DiskFileItemFactory;
import org.apache.commons.fileupload.servlet.ServletFileUpload;
import org.apache.commons.io.IOUtils;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.multipart.support.StandardMultipartHttpServletRequest;
import sun.misc.BASE64Encoder;

import javax.servlet.ServletOutputStream;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.*;
import java.net.URLEncoder;
import java.util.Enumeration;
import java.util.Iterator;
import java.util.List;

/**
 * @className FileUtils.java
 * @author jitwxs
 * @version 创建时间：2018年2月27日 上午9:58:06
 * 依赖commons.io和commons.fileupload
 */
public class FileUtils {
    /**
     * 重命名文件
     * @author jitwxs
     * @version 创建时间：2018年2月27日 上午10:59:33
     * @param path 目录路径
     * @param oldName 源文件名
     * @param newName 目标文件名
     * @return
     */
    public static boolean renameFile(String path, String oldName, String newName) {
        //新的文件名和以前文件名不同时,才有必要进行重命名
        if (!oldName.equals(newName)) {
            File oldfile = new File(path + "/" + oldName);
            File newfile = new File(path + "/" + newName);
            if (!oldfile.exists()) {
                System.out.println("重命名文件失败，" + oldName +"不存在！");
                return false;
            }
            //若在该目录下已经有一个文件和新文件名相同，则不允许重命名
            if (newfile.exists()) {
                System.out.println("重命名文件失败，" + newName + "已经存在！");
                return false;
            } else {
                oldfile.renameTo(newfile);
            }
        }
        return true;
    }

    /**
     * 上传文件(springBoot不可用)
     */
    public String uploadNotSpringBoot(HttpServletRequest request) throws Exception {
        int sizeThreshold = 1024 * 1024;
        File repository = new File("/temp");

        // 创建磁盘文件项工厂，参数为缓存文件大小和临时文件位置
        DiskFileItemFactory factory = new DiskFileItemFactory(sizeThreshold, repository);

        // 创建文件上传核心类
        ServletFileUpload upload = new ServletFileUpload(factory);
        upload.setHeaderEncoding("UTF-8");

        // 判断是否是Multipart类型的
        if (ServletFileUpload.isMultipartContent(request)) {
            // 解析request并获得文件项集合
            List<FileItem> list = upload.parseRequest(request);
            if (list != null) {
                for (FileItem item : list) {
                    // 判断参数是普通参数还是文件参数
                    if (item.isFormField()) {
                        // 获得普通参数的key、value（即formData的fileName和fileSize）
                        String fieldName = item.getFieldName();
                        String fieldValue = item.getString("UTF-8");
                        System.out.println("FormField：k=" + fieldName + ",v=" + fieldValue);
                    } else {
                        //获得文件参数（即formData的file）
                        String fileName = item.getName();
                        String path = "/" + fileName;

                        // 上传文件
                        InputStream in = item.getInputStream();
                        OutputStream out = new FileOutputStream(path);
                        IOUtils.copy(in, out);
                        in.close();
                        out.close();

                        // 删除临时文件
                        item.delete();
                    }
                }
            }
        }
        return "返回给前台的消息";
    }

    /**
     * 上传文件，如果是SpringBoot，配置如下：
     *# 上传单个文件最大允许
     *spring.servlet.multipart.max-file-size=10MB
     *# 每次请求最大允许
     *spring.servlet.multipart.max-request-size=100MB
     */
    public String upload(HttpServletRequest request) throws Exception {
        StandardMultipartHttpServletRequest req = (StandardMultipartHttpServletRequest) request;

        // 遍历普通参数（即formData的fileName和fileSize）
        Enumeration<String> names = req.getParameterNames();
        while (names.hasMoreElements()) {
            String key = names.nextElement();
            String val = req.getParameter(key);
            System.out.println("FormField：k=" + key + "v=" + val);
        }

        // 遍历文件参数（即formData的file）
        Iterator<String> iterator = req.getFileNames();
        while (iterator.hasNext()) {
            MultipartFile file = req.getFile(iterator.next());
            String fileNames = file.getOriginalFilename();
            // 文件名
            fileNames = new String(fileNames.getBytes("UTF-8"));
            //int split = fileNames.lastIndexOf(".");
            // 文件前缀
            //String fileName = fileNames.substring(0, split);
            // 文件后缀
            //String fileType = fileNames.substring(split + 1, fileNames.length());
            // 文件大小
            //Long fileSize = file.getSize();
            // 文件内容
            byte[] content = file.getBytes();

            FileUtils.writeByteArrayToFile(new File(fileNames), content);
        }
        return "返回给前台的消息";
    }

    /**
     * 下载文件
     */
    public void download(HttpServletRequest request, HttpServletResponse response) throws Exception {
        String fileName = request.getParameter("fileName");
        // 文件路径
        String path = "D:\\" + fileName;
        // 得到用于返回给客户端的编码后的文件名
        String agent = request.getHeader("User-Agent");
        String fileNameEncode = solveFileNameEncode(agent, fileName);
        // 客户端判断下载文件类型
        response.setContentType(request.getSession().getServletContext().getMimeType(fileName));
        // 关闭客户端的默认解析
        response.setHeader("Content-Disposition", "attachment;filename=" + fileNameEncode);

        // 下载文件
        ServletOutputStream out = response.getOutputStream();
        InputStream in = new FileInputStream(path);
        int len;
        byte[] buf = new byte[1024];
        while ((len = in.read(buf)) > 0) {
            out.write(buf, 0, len);
        }
        in.close();
    }

    /**
     * 对文件名发送到客户端时进行编码
     */
    private String solveFileNameEncode(String agent, String fileName) {
        String res = "";
        try {
            if (agent.contains("MSIE")) {
                // IE浏览器
                res = URLEncoder.encode(fileName, "utf-8");
                res = res.replace("+", " ");
            } else if (agent.contains("Firefox")) {
                // 火狐浏览器
                BASE64Encoder base64Encoder = new BASE64Encoder();
                res = "=?utf-8?B?"
                        + base64Encoder.encode(fileName.getBytes("utf-8")) + "?=";
            } else {
                // 其它浏览器
                res = URLEncoder.encode(fileName, "utf-8");
            }
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }
        return res;
    }
}
