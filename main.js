document.getElementById("query-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  // 获取表单数据
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const plate = document.getElementById("plate").value;

  // RSA 公钥
  const publicKey = `MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAq2YypaHrQCf1EAufYNd3
  XOAQDoLYLZUKQidHGx5GzP0ds0thgrN4aNnn5s65dKdJv2QK0/GBXo/mJkZJaHrz
  CS5qBRjyHSQ77Lv0M5A1WOiVP/Sw5aMjE1kHP3f/ggJR2wNcZ2RB1g2l9GEPNWr4
  jYt9lgsEizPi1j815Tj0rp6EYPnv5VleZxS2Tr8lf5s8L1NOs7LKGmcHMw78tchj
  Mcj1xiBCj/b5xaVWYZzXSS33KVQReQR9rtZVksE7EVWhFoFyAeRVfcIDpwzt/NDQ
  c2CPFSKNmoJELhWYHbUgY4e7A08d9c2LniNzz4XA+s13923e67PirXUDZ2MW/VKZ
  flkPfbgu0GOCzXsJDkBSlWmJlBeONiAFXeekMgQ71pD+N7g0H47jU/nPTIQM4cz9
  n4ult3e9KhZfiwqQXN2vGe/h+eh02uj07iwF3qCc/X8LEKHQg7+cxrFocAlyknHr
  iWgLz7clohjuOrkcSTe8dlE4PaJBVtt4PiSzfTOY1HF2Ddewjw3LJLC7xcQ/UehB
  blnQGYE7fRRczQ+Lz5BajZNec9i+ZtcQM58HXpEBAvh3jFBZaJj6fMuJ3mFl6Kf7
  LRUNJK6k0NmoQ6OvmoudnIhb7STuBp42HswksaIx5Q6yVqKMEPOtSGj6zIwJpRD6
  4z0/IKzbm4200I4jDvkToKUCAwEAAQ==`;


  //Bug:这里有一个美妙的问题，无人问津
  //AES加密
  //const aeskey = CryptoJS.lib.WordArray.random(32);
  //const vi = CryptoJS.lib.WordArray.random(16);
  
  // 解密
//const decrypted = CryptoJS.AES.decrypt(encrypted, key, {
  //iv: iv,
  //mode: CryptoJS.mode.CBC, // 使用CBC模式
  //padding: CryptoJS.pad.Pkcs7 // 明确指定PKCS#7填充
//});


  // 创建加密函数
  function encrypt(text)   {
    // 使用 RSA 公钥
    const encrypt = new JSEncrypt();
    encrypt.setPublicKey(publicKey);

    // 使用 RSA 公钥加密文本
    const encrypted = encrypt.encrypt(text);

    return encrypted;
}

  // 创建解密函数
  function decrypt(text, key) {
    let decrypted = "";
    for (let i = 0; i < text.length; i++) {
      decrypted += String.fromCharCode(
        text.charCodeAt(i) ^ key.charCodeAt(i % key.length)
      );
    }
    return decrypted;
  }

  // 加密请求数据
  const encrypted_data = encrypt(plate);
  const encrypted_password = encrypt(password);
  console.log("加密的数据:", encrypted_data);
  console.log("加密的密码:", encrypted_password);

  // 组织请求数据
  const data = {
    username: username,
    password: encrypted_password,
    encrypted_data: encrypted_data,
  }

  // 显示等待弹窗
  document.getElementById("loading").style.display = "block";

  try {
    // 发送请求
    const response = await fetch("http://127.0.0.1:5000/api/query", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    // 检查响应状态
    if (!response.ok) {
      throw new Error("服务器返回了错误响应");
    }

// 获取并处理查询结果
const result = await response.json();
const resultsElement = document.getElementById('results');
// 清空之前的结果
resultsElement.innerHTML = '';
if (result.error) {
    // 如果后端返回错误信息
    alert(result.error);
} else if (result.results && result.results.length > 0) {
    // 如果查询有结果
    result.results.forEach(item => {
      // 创建包含结果的div
      const resultDiv = document.createElement('div');
      resultDiv.classList.add('result-item'); // 添加类以便样式化
  
      // 创建车牌号的div，并填充内容
      const plateDiv = document.createElement('div');
      plateDiv.innerHTML = `<span>车牌号：</span><span>${item.id}</span>`;
  
      // 创建所有者的div，并填充内容
      const ownerDiv = document.createElement('div');
      ownerDiv.innerHTML = `<span>所有者：</span><span>${item.owner}</span>`;
  
      // 创建联系电话的div，并填充内容
      const phoneDiv = document.createElement('div');
      phoneDiv.innerHTML = `<span>联系电话：</span><span>${item.phone_number}</span>`;
  
      // 将各个div添加到结果div
      resultDiv.appendChild(plateDiv);
      resultDiv.appendChild(ownerDiv);
      resultDiv.appendChild(phoneDiv);
  
      // 最后，将结果div添加到页面的某个元素中
      resultsElement.appendChild(resultDiv);
  });
  
} else {
    // 如果查询成功但没有结果
    alert('查询成功但没有找到结果');
}

// 显示查询结果
document.getElementById('result').style.display = 'block';
  } catch (error) {
    // 显示错误信息
    alert(error.message);
  } finally {
    // 隐藏等待弹窗
    document.getElementById("loading").style.display = "none";
  }
});
