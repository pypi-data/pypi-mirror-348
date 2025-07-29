var user = null;

function changeUserState(user) {
  $('.logout').removeClass('layui-hide');
  $('.login').addClass('layui-hide');
  $('.username').text(user.username || user.nickName);
  if (user.id == 1) {
    $('.user-admin').removeClass('layui-hide');
  }
}

function checkUser() {
  user = localStorage.getItem('user');
  if (user) {
    user = JSON.parse(user);
    changeUserState(user);
  }
  $.get('/user', function (ret) {
    if (!ret.err) {
      localStorage.setItem('user', JSON.stringify(ret));
      changeUserState(ret);
      user = ret;
    } else {
      $('.logout').addClass('layui-hide');
      $('.login').removeClass('layui-hide');
    }
  })
}

function logout() {
  localStorage.removeItem('user');
  removeCookie('token');
  removeCookie('endpoints');
  $.get('/logout', function () {
    location.href = '/';
  })
}

function copyData(data, msg = "已复制到剪切板") {
  var copyFrom = $('<textarea id="copyFrom">');
  copyFrom.css({
    position: "absolute",
    left: "-1000px",
    top: "-1000px",
  });
  copyFrom.text(data);
  $('body').append(copyFrom);
  copyFrom.select();
  document.execCommand('copy');
  copyFrom.remove();
  layer.msg(msg);
}

function copyBtn(selector) {
  var btnCopy = new ClipboardJS(selector, {
    text: function (trigger) {
      var t = trigger.getAttribute('data-clipboard-text')
      if (trigger.getAttribute('add-host') != null) {
        t = location.protocol + '//' + location.host + t
      }
      return t
    }
  })
  btnCopy.on('success', function (e) {
    layer.msg('已复制到剪贴板', {
      time: 2000
    });
    e.clearSelection();
  })
  btnCopy.on('error', function (e) {
    layer.msg('复制出错，请手动复制', {
      time: 2000
    });
  })
}

function guid() {
  function S4() {
    return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1)
  }
  return (S4() + S4() + "-" + S4() + "-" + S4() + "-" + S4() + "-" + S4() + S4() + S4());
}

function webUpload(selector) {
  var uploadList = $('#upload-list');
  var succeed = true;
  var uploader = WebUploader.create({
    swf: '/static/src/js/Uploader.swf',
    server: location.pathname,
    dnd: document.body,
    disableGlobalDnd: true,
    pick: {
      id: selector,
      innerHTML: '<i class="layui-icon layui-icon-upload"></i><p>点击上传或将文件拖拽到此处</p>',
      multiple: true,
    },
    auto: true,
    prepareNextFile: true,
    compress: false,
    allowMagnify: false,
    crop: false,
    preserveHeaders: false,
    chunked: true,
    chunkSize: 5 * 1024 * 1024,
    chunkRetry: 5,
    threads: 10,
    formData: {
      token: (function () { return getCookie('token') || ''; })(),
      guid: (function () { return guid(); })(),
    },
    fileNumLimit: 100,
    duplicate: true,
  });

  uploader.on('fileQueued', function (file) {
    if (file.source.source.webkitRelativePath) {
      file.name = file.source.source.webkitRelativePath;
    }
    uploadList.parents('table').removeClass('layui-hide');
    var html = $(['<tr id="' + file.id + '">'
      , '<td style="text-align:left !important">' + file.name + '</td>'
      , '<td style="width:80px">' + (file.size / 1014).toFixed(1) + 'kb</td>'
      , '<td style="width:80px">准备上传</td>'
      , '<td style="width:100px">'
      , '<button class="layui-btn layui-btn-xs file-reload">重传</button>'
      , '<button class="layui-btn layui-btn-xs layui-btn-danger file-remove">删除</button>'
      , '</td>'
      , '<td style="width:300px">'
      , '<div class="layui-progress" lay-filter="' + file.id + '" lay-showPercent="true"><div class="layui-progress-bar" lay-percent="0%"></div></div>'
      , '</td>'
      , '</tr>'].join(''));
    uploadList.append(html);

    uploader.md5File(file)
      .progress(function (percent) {
        element.progress(file.id, (percent * 100).toFixed(1) + '%');
      })
      .then(function (md5) {
        file.md5 = md5;
      });
  });

  uploader.on('uploadProgress', function (file, percent) {
    var tr = uploadList.find('tr#' + file.id)
      , tds = tr.children();
    tds.eq(2).html('<span style="color: #5FB878;">正在上传</span>');
    element.progress(file.id, (percent * 100).toFixed(1) + '%');
  });
  uploader.on('uploadSuccess', function (file, ret) {
    console.log('upload succeed' + file.id)
    var tr = uploadList.find('tr#' + file.id)
      , tds = tr.children();
    if (file.size > uploader.options.chunkSize) {
      var data = {
        action: 'merge',
        id: file.id,
        size: file.size,
        name: file.name,
        md5: file.md5,
      };
      for (var i in uploader.options.formData) {
        data[i] = uploader.options.formData[i];
      }
      $.post(location.pathname, data, function (ret) {
        if (ret.err == 0) {
          tds.eq(2).html('<span style="color: #5FB878;">上传成功</span>');
        } else {
          tds.eq(2).html('<span style="color: #FF5722;">上传失败</span>');
          succeed = false;
        }
      })
    } else {
      if (ret.err == 0) {
        tds.eq(2).html('<span style="color: #5FB878;">上传成功</span>');
      } else {
        tds.eq(2).html('<span style="color: #FF5722;">上传失败</span>');
        succeed = false;
      }
    }
  });

  uploader.on('uploadError', function (file) {
    var tr = uploadList.find('tr#' + file.id)
      , tds = tr.children();
    tds.eq(2).html('<span style="color: #FF5722;">上传失败</span>');
    succeed = false;
  })

  uploader.on('uploadFinished', function () {
    setTimeout(function () {
      if (succeed) location.reload()
    }, 1000)
  })

  $(document).on('click', 'tr .file-reload', function () {
    uploader.upload(uploader.getFile($(this).parents('tr').attr("id"), true));
  })
  $(document).on('click', 'tr .file-remove', function () {
    var tr = $(this).parents('tr');
    uploader.removeFile(uploader.getFile(tr.attr("id"), true));
    tr.remove();
  })
  $(document).on('change', 'input[webkitdirectory]', function () {
    console.log('upload ' + this.files.length + ' files');
    if (this.files.length > 100) {
      layer.msg('每次最多上传100个文件');
    } else {
      uploader.addFiles(this.files);
    }
  })
}

layui.use(['layer', 'element', 'tree', 'form'], function () {
  layer = layui.layer;
  element = layui.element;
  form = layui.form;
  $ = layui.$;

  copyBtn('.btn-copy');
  webUpload('#upload-box');

  $(function () {
    checkUser();

    var masonryNode = $('#masonry');
    if (masonryNode.length >= 1) {
      masonryNode.imagesLoaded(function () {
        masonryNode.masonry({
          itemSelector: '.layui-col-md2',
          columnWidth: '.layui-col-md2',
          isAnimated: true,
        });
      });
    }

    /*
    if($('#upload-box').length >= 1){
      $(document).on({
        paste: function (e) {
          e.stopPropagation();
          e.preventDefault();
          var clipboardData = (e.clipboardData || e.originalEvent.clipboardData);
          if (clipboardData.items) {
            var text = clipboardData.getData('text')
            if (text.search(/https?:\/\//i) >= 0){
              var data = {'action': 'download', 'src': text}
              layer.msg('正在下载...', {time: 600000})
              $.post(location.pathname, data, function(ret){
                if(ret.msg) layer.msg(ret.msg)
              })
            } else {
              layer.msg('只支持http或https下载链接');
            }
          }
        }
      })
    }
    */

    if (getCookie('tree')) {
      $.get(location.pathname + '?f=tree', function (ret) {
        layui.tree.render({
          elem: '#tree',
          accordion: true,
          isJump: true,
          data: ret.nodes,
        })
      })
    }

    $(document).on('click', '.user-logout', function () {
      logout();
    })

    $(document).on('mouseover', '.layui-card', function () {
      $(this).find('.action').removeClass('layui-hide')
    })

    $(document).on('mouseleave', '.layui-card', function () {
      $(this).find('.action').addClass('layui-hide')
    })

    $(document).on("mouseover", '.layui-tips', function () {
      var that = this;
      layer.tips($(this).attr('tips'), that, { tips: 1 });
    })

    $(document).on("mouseleave", '.layui-tips', function () {
      layer.closeAll('tips');
    })

    $(document).on("click", ".tree-toggle", function () {
      if (getCookie("tree")) {
        removeCookie("tree")
        $('.tree-toggle i').removeClass("layui-icon-shrink-right").addClass("layui-icon-spread-left")
        $("#tree").addClass("layui-hide")
        $(".tree-table").addClass("layui-col-md12").removeClass("layui-col-md10")
      } else {
        setCookie("tree", "on")
        $('.tree-toggle i').removeClass("layui-icon-spread-left").addClass("layui-icon-shrink-right")
        $("#tree").removeClass("layui-hide")
        $(".tree-table").addClass("layui-col-md10").removeClass("layui-col-md12")
        $.get(location.pathname + '?f=tree', function (ret) {
          layui.tree.render({
            elem: '#tree',
            accordion: true,
            isJump: true,
            data: ret.nodes,
          });
        })
      }
    })

    $(document).on("click", ".batch-folder", function () {
      layer.prompt({
        closeBtn: 2,
        shadeClose: true,
        maxlength: 100,
        value: '',
        title: '请输入文件夹名',
        area: ['200px', '50px'],
      }, function (value, index, elem) {
        $.post(location.pathname, { 'action': 'folder', 'name': $.trim(value) }, function (ret) {
          if (ret.err) layer.msg(ret.msg)
          else {
            layer.msg('创建文件夹成功')
            location.reload()
          }
        })
      })
    })

    $(document).on("click", ".batch-tools", function () {
      $(".toggle-tools").toggleClass("layui-hide");
      if (getCookie("tools")) {
        removeCookie("tools")
      } else {
        setCookie("tools", "on")
      }
    })

    $(document).on("click", ".batch-preview", function () {
      if (getCookie("preview") == "on") {
        setCookie("preview", "off")
      } else {
        setCookie("preview", "on")
      }
      location.reload()
    })

    $(document).on('click', '.batch-display', function () {
      if (getCookie("table")) {
        removeCookie("table")
      } else {
        setCookie("table", "on")
      }
      location.reload()
    })

    $(document).on('click', 'td input[type=checkbox]', function () {
      $(this).parents('tr').toggleClass('selected')
      var selected = $('.filelist tbody tr input[type=checkbox]:checked').length
      if (selected == $('.filelist tbody tr').length) {
        $('.batch-select').prop('indeterminate', false)
        $('.batch-select').prop('checked', true)
      } else if (selected == 0) {
        $('.batch-select').prop('indeterminate', false)
        $('.batch-select').prop('checked', false)
      } else {
        $('.batch-select').prop('indeterminate', true)
      }
    })

    $(document).on('click', '.btn-checkbox', function (e) {
      if ($(e.target).is('input[type=checkbox]')) {
        return;
      }

      var checkbox = $(this).find('input[type=checkbox]')
      checkbox.prop('checked', !checkbox.prop('checked'))

      $(this).parents('tr').toggleClass('selected')
      var selected = $('.filelist tbody tr input[type=checkbox]:checked').length
      if (selected == $('.filelist tbody tr').length) {
        $('.batch-select').prop('indeterminate', false)
        $('.batch-select').prop('checked', true)
      } else if (selected == 0) {
        $('.batch-select').prop('indeterminate', false)
        $('.batch-select').prop('checked', false)
      } else {
        $('.batch-select').prop('indeterminate', true)
      }
    })

    $(document).on('click', '.batch-select', function () {
      var checked = $(this).prop('checked')
      $('.filelist tbody tr').each(function () {
        $(this).find('input[type=checkbox]').prop('checked', checked);
        if (checked) {
          $(this).addClass('selected')
        } else {
          $(this).removeClass('selected')
        }
      })
    })

    $(document).on('click', '.batch-unselect', function () {
      $('.filelist tbody tr').each(function () {
        var checkbox = $(this).find("input[type=checkbox]")
        checkbox.prop('checked', !checkbox.prop('checked'))
        $(this).toggleClass('selected')
      })
    })

    $(document).on('click', '.batch-action', function () {
      var action = $(this).attr('action');
      var selected = $('.filelist tbody tr input[type=checkbox]:checked').length;
      var text = `批量处理${selected}个文件`;
      if (action == 'delete') {
        text = `批量删除${selected}个文件`;
      } else if (action == 'share') {
        text = `批量分享${selected}个文件`;
      }
      layer.confirm(text, {
        title: '确定执行',
        icon: 3,
        shadeClose: true,
        closeBtn: 2,
      }, function (index) {
        layer.close(index);
        $(".filelist tr").each(function () {
          if ($(this).find('input[type=checkbox]:checked').length > 0) {
            var tr = $(this);
            var url = $(this).find(".file-link").data("url");
            if (url != undefined) {
              $.post(url, { 'action': action, 'batch': 'on' }, function (ret) {
                if (ret.msg) layer.msg(ret.msg)
                if (action == 'delete') tr.slideUp();
              })
            }
          }
        })
      })
    })

    $(document).on('click', '.btn-enter', function (event) {
      event.preventDefault();
      var link = $(this).parents('tr').find('.file-link').length > 0 ? $(this).parents('tr').find('.file-link') : $(this).parents('.layui-card-body').find('.file-link');
      var url = link.attr('href');
      if (link.hasClass('dir-link')) {
        location.href = url;
      } else {
        if (url.indexOf('?') >= 0) url += '&f=preview';
        else url += '?f=preview';
        var width = window.innerWidth > 768 ? parseInt(window.innerWidth * 0.7) : parseInt(window.innerWidth * 0.8);
        var height = window.innerWidth > 768 ? parseInt(window.innerHeight * 0.8) : parseInt(window.innerHeight * 0.7);
        layer.open({
          type: 2,
          title: false,
          content: url,
          shadeClose: true,
          closeBtn: 2,
          area: [`${width}px`, `${height}px`],
          success: function (layero, index) {
            // var css = {"max-width": "100%", "max-height": "100%", "margin": "20px auto"};
            // $($("iframe").contents().find("body")).children("img:first").css(css);
            // layer.iframeAuto(index);
          }
        })
      }
    })

    $(document).on("click", ".btn-link", function () {
      var link = $(this).parents('tr').find('.file-link').length > 0 ? $(this).parents('tr').find('.file-link') : $(this).parents('.layui-card-body').find('.file-link');
      var url = link.data('url');
      copyData(location.protocol + '//' + location.host + url);
    })

    $(document).on("click", ".btn-rename", function () {
      var link = $(this).parents('tr').find('.file-link').length > 0 ? $(this).parents('tr').find('.file-link') : $(this).parents('.layui-card-body').find('.file-link');
      var url = link.data('url');
      var name = $.trim(link.text());
      layer.prompt({
        closeBtn: 2,
        shadeClose: true,
        value: name,
        title: '请输入新文件名',
        area: ['200px', '50px'],
      }, function (value, index, elem) {
        var data = { 'action': 'rename', 'filename': $.trim(value) };
        $.post(url, data, function (ret) {
          layer.close(index);
          if (ret.err) layer.msg(ret.msg)
          else {
            layer.msg('重命名成功');
            location.reload();
          }
        })
      })
    })

    $(document).on("click", ".btn-move", function () {
      var link = $(this).parents('tr').find('.file-link').length > 0 ? $(this).parents('tr').find('.file-link') : $(this).parents('.layui-card-body').find('.file-link');
      var url = link.data('url');
      layer.prompt({
        closeBtn: 2,
        shadeClose: true,
        value: '',
        title: '请输入完整的文件夹路径',
        area: ['200px', '50px'],
      }, function (value, index, elem) {
        var data = { 'action': 'move', 'dirname': $.trim(value) }
        $.post(url, data, function (ret) {
          layer.close(index);
          if (ret.err) layer.msg(ret.msg)
          else {
            layer.msg('移动文件成功');
            location.reload();
          }
        })
      })
    })

    $(document).on("click", ".btn-info", function () {
      var link = $(this).parents('tr').find('.file-link').length > 0 ? $(this).parents('tr').find('.file-link') : $(this).parents('.layui-card-body').find('.file-link');
      var url = link.data('url');
      var name = $.trim(link.text());
      var md5 = $(this).data('md5');
      $.get(url, { 'f': 'info', 'v': Math.round(Math.random() * 99999) }, function (ret) {
        if (md5) {
          var content = '<p><b>md5:</b> ' + md5 + '</p>';
        } else {
          var content = '<p><b>type:</b> folder</p>';
        }
        if (ret.share != undefined) {
          content += '<p><b>share:</b> ' + ret.share + '</p>'
        }
        layer.open({
          closeBtn: 2,
          shaderClose: true,
          title: name,
          content: content
        })
      })
    })

    $(document).on("click", ".btn-action", function () {
      var link = $(this).parents('tr').find('.file-link').length > 0 ? $(this).parents('tr').find('.file-link') : $(this).parents('.layui-card-body').find('.file-link');
      var url = link.data('url');
      var action = $(this).attr("action");
      var text = $(this).attr("text");
      if (text) layer.msg(text, { time: 30000 });
      $.post(url, { 'action': action }, function (ret) {
        if (ret.msg) layer.msg(ret.msg)
      })
    })

    $(document).on("click", ".btn-share", function () {
      var link = $(this).parents('tr').find('.file-link').length > 0 ? $(this).parents('tr').find('.file-link') : $(this).parents('.layui-card-body').find('.file-link');
      var url = link.data('url');
      var share = $(this).data('share');
      if (share == undefined) {
        layer.prompt({
          closeBtn: 2,
          shadeClose: true,
          value: '',
          title: '请输入分享天数，输入空则不过期',
          area: ['200px', '50px'],
        }, function (value, index, elem) {
          layer.close(index);
          var data = { 'action': 'share', 'days': $.trim(value) };
          $.post(url, data, function (ret) {
            if (ret.msg) layer.msg(ret.msg)
            else layer.msg('分享成功')
            location.reload()
          })
        })
      } else {
        var text = url.substring(url.lastIndexOf('/') + 1)
        layer.confirm(text, {
          title: '取消分享',
          icon: 3,
          shadeClose: true,
          closeBtn: 2,
        }, function () {
          var data = { 'action': 'unshare' };
          $.post(url, data, function (ret) {
            if (ret.msg) layer.msg(ret.msg)
            else layer.msg('取消分享成功')
            location.reload()
          })
        })
      }
    })

    $(document).on("click", ".btn-delete", function () {
      var link = $(this).parents('tr').find('.file-link').length > 0 ? $(this).parents('tr').find('.file-link') : $(this).parents('.layui-card-body').find('.file-link');
      var url = link.attr('href');
      var text = link.attr('title');
      layer.confirm(text, {
        title: '确定删除',
        icon: 3,
        shadeClose: true,
        closeBtn: 2,
      }, function (index) {
        var data = { 'action': 'delete' };
        if (url != undefined) {
          $.post(url, data, function (ret) {
            layer.close(index);
            if (ret.err) layer.msg(ret.msg);
            else {
              layer.msg('删除成功');
              location.reload();
            }
          })
        }
      })
    })

    $(document).on('click', '.btn-manage', function () {
      var id = $(this).parents('tr').data('id');
      var action = $(this).attr('action')
      $.post(location.pathname, {
        id: id,
        action: action
      }, function (ret) {
        if (ret.err) layer.msg(ret.msg);
        else location.reload();
      })
    })

    $(document).on('click', '.btn-email', function () {
      var email = $(this)
        .parents(".layui-form")
        .find("input[name=email]")
        .val();
      layer.msg('发送中，请稍后', { time: 60000 });
      $.post('/email/check', { 'email': email }, function (ret) {
        if (ret.err) layer.msg(ret.msg)
        else layer.msg('发送验证码成功')
      })
    })

    $(document).on('click', '.weixin-login', function () {
      var id = $(this).data('id');
      var url = "https://wx.ishield.cn/qrcode";
      var token = getCookie("token") || "";
      $.get(url, { site_id: id, token: token }, function (ret) {
        if (ret.err) {
          layer.msg(ret.msg);
        } else {
          var counter = 0;
          var timer = setInterval(function () {
            counter += 1;
            $.get("/check", { scene: ret.check }, function (res) {
              if (res.err == 0) {
                clearInterval(timer);
                var next = parseUrl().params.next;
                if (next) {
                  location.href = decodeURIComponent(next);
                } else {
                  location.href = "/admin";
                }
              } else if (res.err == 2) {
                clearInterval(timer);
                layui.layer.alert(res.msg);
              }
              if (counter >= 1800) {
                clearInterval(timer);
              }
            });
          }, 2000);
          layer.open({
            type: 1,
            title: false,
            area: ["300px", "300px"],
            offset: "200px",
            shadeClose: true,
            closeBtn: 2,
            shade: 0.5,
            id: "LAY_layuipro",
            moveType: 1,
            content: '<img width="300" height="300" src="' + ret.code + '">',
            cancel: function (index, layero) {
              clearInterval(timer);
            },
          });
        }
      });
    });

    form.verify({
      confirmPassword: function (value, item) {
        var password = $(item).parents('form').find('input[name=password]').val();
        if (value !== password) {
          return '两次密码输入不一致';
        }
      }
    });

    form.on('submit(default)', function (data) {
      var text = $(this).text();
      var btn = $(this);
      $(this).text('正在提交').addClass('layui-btn-disabled');
      $.ajax({
        type: data.form.getAttribute('method'),
        url: data.form.getAttribute('action'),
        data: data.field,
        success: function (ret) {
          var next = parseUrl().params.next;
          if (ret.err) layer.msg(ret.msg);
          else if (next || data.form.getAttribute('href')) {
            layer.msg('提交成功，重定向页面中');
            setTimeout(function () {
              if (next) {
                location.href = decodeURIComponent(next);
              } else {
                location.href = data.form.getAttribute('href');
              }
            }, 1000);
          }
          else if (data.form.getAttribute("reload")) {
            layer.msg('提交成功, 刷新页面中');
            setTimeout(function () {
              location.reload();
            }, 1000)
          } else {
            layer.msg('提交成功');
          }
        },
        error: function () {
          layer.msg('提交失败');
        },
        complete: function () {
          btn.text(text).removeClass('layui-btn-disabled');
        }
      })
      return false;
    })

  })
})
