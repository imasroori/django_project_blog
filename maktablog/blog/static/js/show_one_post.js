box_type_comment = document.getElementById("box-type-comment")
btn_like = document.getElementById("like")
btn_dislike = document.getElementById("dislike")
star_post = document.getElementById("star-post")
send_comment = document.getElementById("send-comment")
commentForm = document.getElementById('commentForm')

btn_like_comment = document.getElementById("like-comment")
btn_dislike_comment = document.getElementById("dislike-comment")

star_post.addEventListener("click", function(){
                                    if(this.getAttribute("data-login") == 'loggedout'){

                                    this.setAttribute("data-toggle","modal")
                                    this.setAttribute("data-target","#myModal")

                                    }else{
                                    var post_id = this.getAttribute("data-post-id")
                                    $.ajax({
                                    type:'GET',
                                    url:'/api/star_post',
                                    data:{

                                        'post_id':post_id ,

                                        },
                                        datatype:'json',
                                        success:function(data){
                                        if (data.is_stared){
                                        star_post.classList.remove('fa-star')
                                        star_post.classList.add('fa-star-o')
                                        console.log('شما پست را از حالت ذخیره خارج کردید')
                                                 }else{
                                                   star_post.classList.remove('fa-star-o')
                                                   star_post.classList.add('fa-star')
                                                   console.log('شما پست را ذخیره کردید')

                                                 }
                                        }

                                    })

                                    }
                                                 });


box_type_comment.addEventListener('click',function(){

                                    if(this.getAttribute("data-login") == 'loggedout'){

                                    this.setAttribute("data-toggle","modal")
                                    this.setAttribute("data-target","#myModal")

                                    }else{

                                    }
                                    })



btn_like.addEventListener("click",function(){

                                    if(this.getAttribute("data-login") == 'loggedout'){

                                    this.setAttribute("data-toggle","modal")
                                    this.setAttribute("data-target","#myModal")

                                    }else{
                                    var post_id = this.getAttribute("data-post-id")

                                            $.ajax({
                                            type:'GET',
                                            url:'/api/like_post',
                                            data:{
                                            'post_id':post_id,
                                            },
                                            datatype:'json',
                                            success:function(data){
                                            if (data.is_liked){
                                            console.log("شما این پست را پسندیده اید")
                                            var value_likes = $('.value-likes')[0].innerHTML
                                            value_likes = +value_likes-1
                                            $('.value-likes')[0].innerHTML = value_likes
                                            btn_like.classList.remove('btn-outline-success')

                                            }else{
                                            console.log("شما این پست را پسندیدید")
                                            var value_likes = $('.value-likes')[0].innerHTML
                                            value_likes = +value_likes+1
                                            $('.value-likes')[0].innerHTML = value_likes
                                            btn_like.classList.add('btn-outline-success')

                                                if(data.is_in_disliked){
                                                btn_dislike.classList.remove('btn-outline-danger')
                                                var value_dislikes = $('.value-dislikes')[0].innerHTML
                                                value_dislikes = +value_dislikes-1
                                                $('.value-dislikes')[0].innerHTML = value_dislikes
                                                }
                                            }

                                                }
                                            })


                                    }
                                    })



btn_dislike.addEventListener("click",function(){

                                    if(this.getAttribute("data-login") == 'loggedout'){

                                    this.setAttribute("data-toggle","modal")
                                    this.setAttribute("data-target","#myModal")

                                    }else{

                                    var post_id = this.getAttribute("data-post-id")

                                            $.ajax({
                                            url:'/api/dislike_post',
                                            data:{
                                            'post_id':post_id,
                                            },
                                            datatype:'json',
                                            success:function(data){
                                            if (data.is_disliked){
                                            console.log("شما این پست را نپسندیده اید")
                                            var value_dislikes = $('.value-dislikes')[0].innerHTML
                                            value_dislikes = +value_dislikes-1
                                            $('.value-dislikes')[0].innerHTML = value_dislikes
                                            btn_dislike.classList.remove('btn-outline-danger')

                                            }else{
                                            console.log("شما این پست را پسندیدید")
                                            var value_dislikes = $('.value-dislikes')[0].innerHTML
                                            value_dislikes = +value_dislikes+1
                                            $('.value-dislikes')[0].innerHTML = value_dislikes
                                            btn_dislike.classList.add('btn-outline-danger')
                                                if(data.is_in_liked){
                                                btn_like.classList.remove('btn-outline-success')
                                                var value_likes = $('.value-likes')[0].innerHTML
                                                value_likes = +value_likes-1
                                                $('.value-likes')[0].innerHTML = value_likes
                                                }


                                            }

                                                }
                                            })


                                    }
                                    })



commentForm.addEventListener('submit',function(e){
                                            e.preventDefault()
                                            var commentBody = $('#commentBody')
                                            var post_id = this.getAttribute("data-post-id")
                                            if (commentBody.val() == 0){
                                            alert('شما نمی توانید نظر خالی ثبت کنید!')
                                            }else{
                                            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                                            $.ajax({

                                            url:'/api/comment_post_form',
                                            headers: {'X-CSRFToken': csrftoken},
                                            type: "POST",
                                            data:{
                                            'post':post_id,
                                            'text':commentBody.val(),
                                            },
                                            datatype:'json',
                                            success:function(data){
                                            alert("نظر شما با موفقیت ثبت شد، پس از تایید مدیر در سایت نمایش داده می شود. با تشکر از شما")

                                             var cb = $("#commentBody")[0]
                                            cb.value=""
                                            }
                                            })
                                            }



                                            })


                                





function myFunction1(d){

                                    if(d.getAttribute("data-login") == 'loggedout'){

                                    d.setAttribute("data-toggle","modal")
                                    d.setAttribute("data-target","#myModal")

                                    }else{
                                    let commentid = d.getAttribute("data-comment-id")

                                    let vallike = '.val-like-comment-'+ commentid
                                    let valdislike = '.val-dislike-comment-'+ commentid

                                    let xdislike = document.getElementById("dislike-comment-"+commentid)
                                            $.ajax({
                                            type:'GET',
                                            url:'/api/like_comment',
                                            data:{

                                            'comment_id':commentid,
                                            },
                                            datatype:'json',
                                            success:function(data){
                                            if (data.is_liked){
                                            console.log("شما این نظر را پسندیده اید")
                                            let valuelikescomment = $(vallike)[0].innerHTML
                                            valuelikescomment = +valuelikescomment-1
                                            $(vallike)[0].innerHTML = valuelikescomment

                                            d.classList.remove('btn-outline-success')

                                            }else{
                                            console.log("شما این پست را پسندیدید")
                                            let valuelikescomment = $(vallike)[0].innerHTML
                                            valuelikescomment = +valuelikescomment+1
                                            $(vallike)[0].innerHTML = valuelikescomment
                                            d.classList.add('btn-outline-success')

                                                if(data.is_in_disliked){
                                                xdislike.classList.remove('btn-outline-danger')
                                                let valuedislikescomment = $(valdislike)[0].innerHTML
                                                valuedislikescomment = +valuedislikescomment-1
                                                $(valdislike)[0].innerHTML = valuedislikescomment
                                                }
                                            }

                                                }
                                            })


                                    }


}
function myFunction2(d){
                        if(d.getAttribute("data-login") == 'loggedout'){

                        d.setAttribute("data-toggle","modal")
                        d.setAttribute("data-target","#myModal")

                        }else{
                        let commentid = d.getAttribute("data-comment-id")
                        let vallike = '.val-like-comment-'+commentid
                        let valdislike = '.val-dislike-comment-'+ commentid
                        let xlike = document.getElementById("like-comment-"+commentid)

                                $.ajax({
                                type:'GET',
                                url:'/api/dislike_comment',
                                data:{
                                'comment_id':commentid,
                                },
                                datatype:'json',
                                success:function(data){
                                if (data.is_disliked){
                                console.log("شما این نظر را نپسندیده اید")
                                let valuedislikescomment = $(valdislike)[0].innerHTML
                                valuedislikescomment = +valuedislikescomment-1
                                $(valdislike)[0].innerHTML = valuedislikescomment
                                d.classList.remove('btn-outline-danger')

                                }else{
                                console.log("شما این پست را نپسندیدید")
                                let valuedislikescomment = $(valdislike)[0].innerHTML
                                valuedislikescomment = +valuedislikescomment+1
                                $(valdislike)[0].innerHTML = valuedislikescomment
                                d.classList.add('btn-outline-danger')

                                    if(data.is_in_liked){
                                    xlike.classList.remove('btn-outline-success')
                                    let valuelikescomment = $(vallike)[0].innerHTML
                                    valuelikescomment = +valuelikescomment-1
                                    $(vallike)[0].innerHTML = valuelikescomment
                                    }
                                }

                                    }
                                })


                        }


}
