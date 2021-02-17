
box_type_comment = document.getElementById("box-type-comment")
btn_like = document.getElementById("like")
btn_dislike = document.getElementById("dislike")
star_post = document.getElementById("star-post")
send_comment = document.getElementById("send-comment")
commentForm = document.getElementById('commentForm')

star_post.addEventListener("click", function(){
                                    if(this.getAttribute("data-login") == 'loggedout'){

                                    this.setAttribute("data-toggle","modal")
                                    this.setAttribute("data-target","#myModal")

                                    }else{
                                    var post_id = this.getAttribute("data-post-id")
                                    $.ajax({

                                    url:'/ajax/star_post',
                                    data:{

                                        'post_id':post_id ,

                                        },
                                        datatype:'json',
                                        success:function(data){
                                        if (data.is_stared){
                                        star_post.classList.remove('fa-star')
                                        star_post.classList.add('fa-star-o')
                                                 }else{
                                                   star_post.classList.remove('fa-star-o')
                                                   star_post.classList.add('fa-star')

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
                                    var like_dislike_id = this.id
                                            $.ajax({
                                            url:'/ajax/like_dislike_post',
                                            data:{
                                            'post_id':post_id,
                                             'like_dislike':like_dislike_id,
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
                                    var like_dislike_id = this.id

                                            $.ajax({
                                            url:'/ajax/like_dislike_post',
                                            data:{
                                            'post_id':post_id,
                                            'like_dislike':like_dislike_id,
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



